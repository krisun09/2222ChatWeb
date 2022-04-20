// hash and salt the password
// generate RSA key pairs
// export public key and send it to the server
// export private key and store it locally
// test set cookies

function setCookie(key, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = key + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(key) {
    var keyEQ = key + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(keyEQ) == 0) return c.substring(keyEQ.length,c.length);
    }
    return null;
}

function setLocalStorage(key, value) {
    localStorage.setItem(key, value);
}

function getLocalStorage(key) {
    var value = localStorage.getItem(key)
    return value
}

function setSessionStorage(key, value) {
    sessionStorage.setItem(key, value);
    alert('username successfully stored')
}

function getSessionStorage(key) {
    var value = sessionStorage.getItem(key)
    return value
}

function listen() {
    const input = document.querySelector('input');
    const data = document.getElementById("pwd");

    input.addEventListener('input', sendToPy(data));
}

function sendToPy(data) {
    data = encryptMessage(data);
    el.dispatchEvent(data);
}

// ---------------------------------------------------------- //
// signing purposes, ref: https://github.com/mdn/dom-examples/blob/master/web-crypto/sign-verify/rsassa-pkcs1.js
// ---------------------------------------------------------- //

/*
  Store the calculated signature here, so we can verify it later.
*/
//let signature;

/*
  Fetch the contents of the "message" textbox, and encode it
  in a form we can use for sign operation.
*/
function getMessageEncoding() {
    const messageBox = document.querySelector("#rsassa-pkcs1-message");
    let message = messageBox.value;
    let enc = new TextEncoder();
    return enc.encode(message);
}

/*
Get the encoded message-to-sign, sign it and display a representation
of the first part of it in the "signature" element.
*/
async function signMessage(privateKey) {
    const signatureValue = document.querySelector(".rsassa-pkcs1 .signature-value");
    signatureValue.classList.remove("valid", "invalid");

    let encoded = getMessageEncoding();
    signature = await window.crypto.subtle.sign(
        "RSASSA-PKCS1-v1_5",
        privateKey,
        encoded
    );

    signatureValue.classList.add('fade-in');
    signatureValue.addEventListener('animationend', () => {
        signatureValue.classList.remove('fade-in');
    });
    let buffer = new Uint8Array(signature, 0, 5);
    signatureValue.textContent = `${buffer}...[${signature.byteLength} bytes total]`;
}

/*
Fetch the encoded message-to-sign and verify it against the stored signature.
* If it checks out, set the "valid" class on the signature.
* Otherwise set the "invalid" class.
*/
async function verifyMessage(publicKey) {
    const signatureValue = document.querySelector(".rsassa-pkcs1 .signature-value");
    signatureValue.classList.remove("valid", "invalid");

    let encoded = getMessageEncoding();
    let result = await window.crypto.subtle.verify(
        "RSASSA-PKCS1-v1_5",
        publicKey,
        signature,
        encoded
    );

    signatureValue.classList.add(result ? "valid" : "invalid");
}

function sign_message(){
    /*
    Generate a sign/verify key, then set up event listeners
    on the "Sign" and "Verify" buttons.
    */
    window.crypto.subtle.generateKey(
        {
        name: "RSASSA-PKCS1-v1_5",
        // Consider using a 4096-bit key for systems that require long-term security
        modulusLength: 2048,
        publicExponent: new Uint8Array([1, 0, 1]),
        hash: "SHA-256",
        },
        true,
        ["sign", "verify"]
    ).then((keyPair) => {
        const signButton = document.querySelector(".rsassa-pkcs1 .sign-button");
        signButton.addEventListener("click", () => {
            signMessage(keyPair.privateKey);
        });

        const verifyButton = document.querySelector(".rsassa-pkcs1 .verify-button");
        verifyButton.addEventListener("click", () => {
            verifyMessage(keyPair.publicKey);
        });
    });
};


// ---------------------------------------------------------- //
// generate user key pair, enc and dec
// ---------------------------------------------------------- //

async function generateKeyPairs() {
    return window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256",
        },
        true,
        ['encrypt', 'decrypt']
    );
}

async function importPublicKey(jwk) {
    console.log("this is jwk");
    console.log(jwk);
    return window.crypto.subtle.importKey(
        'jwk',
        jwk,
        {
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
      true,
      ['encrypt']
    );
  }

async function importPrivateKey(jwk) {
    return window.crypto.subtle.importKey(
        'jwk',
        jwk,
        {
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
      true,
      ['decrypt']
    );
  }

async function exportCryptoKey(key) {
    return window.crypto.subtle.exportKey(
        "jwk",
        key
    );
}


async function encryptMessage(msg, public_key){
    // msg is the text we want to encrypt
    // public_key is the friend who you want to talk to 's public key
    console.log("this is the public key");
    console.log(public_key);
    let pub_key = await window.importPublicKey(public_key);

    var encoded_msg = window.str2ab(msg);

    return crypto.subtle.encrypt(
        {
            name: 'RSA-OAEP'
        },
        pub_key,
        encoded_msg // data that want to encrypt -- should be an array buffer format
    );
}

async function decryptMessage(encrypted_msg, private_key){
    console.log("this is the private key");
    console.log(private_key);
    let pri_key = await window.importPrivateKey(private_key);

    return crypto.subtle.decrypt(
        {
            name: 'RSA-OAEP'
        },
        pri_key,
        encrypted_msg
    );
}

function ab2str(buf) {
    return String.fromCharCode.apply(null, new Uint8Array(buf));
}
function str2ab(str) {
    var buf = new ArrayBuffer(str.length*2); // 2 bytes for each char
    var bufView = new Uint8Array(buf);
    for (var i=0, strLen=str.length; i < strLen; i++) {
    bufView[i] = str.charCodeAt(i);
    }
    return buf;
}


let key = await window.generateKeyPairs();

let public_key = key.publicKey;
let private_key = key.privateKey;

let exported_pub = await window.exportCryptoKey(public_key);
setSessionStorage.setItem('puk', exported_pub);

let exported_pri = await window.exportCryptoKey(private_key);
// Store private key in cookies for 15 days
//setCookie('user', exported_pri, 15);
setLocalStorage("prik", exported_pri);


console.log("excuted");
console.log(decrtpted_result);
console.log(window.ab2str(decrtpted_result));