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

function generateKeyPairs(username) {
    return crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256",
        },
        true,
        ['encrypt', 'decrypt']
    )
    .then(function(key){
        var output = "now you have a key pair:  "
        var public_key = key.publicKey;
        var private_key = key.privateKey;

        if (public_key == undefined){
            output += "public key generate fail ";
        } else{
            output += "public key generate succeed ";
        }
        if (private_key == undefined){
            output += "private key generate fail";
        }else{
            output += "private key generate succeed ";

        }

        alert(output); //testing

        // export key value
        var pubk = window.exportCryptoKey(public_key);

        sessionStorage.setItem('puk', public_key)

        var prik = window.exportCryptoKey(private_key);

        // Store private key in cookies for 15 days
        setCookie('prik', prik, 15)

        var encrypted = window.encryptMessage("hello", pubk);
        window.decryptMessage(encrypted, prik);

    })
    .catch(function(err){
        console.log(err);
    })
}


async function importPublicKey(jwk) {
    return await window.crypto.subtle.importKey(
        "jwk",
        jwk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
      true,
      ['encrypt']
    )
    .then(function(publickey){
        console.log(publickey);
    })
    .catch(function(err){
        console.log(err);
    })
  }

async function importPrivateKey(jwk) {
    return await window.crypto.subtle.importKey(
        "jwk",
        jwk,
        {
            name: "RSA-OAEP",
            hash: "SHA-256"
        },
      true,
      ['decrypt']
    )
    .then(function(privatekey){
        console.log(privatekey);
    })
    .catch(function(err){
        console.log(err);
    })
  }

async function exportCryptoKey(key) {
    const exported = await window.crypto.subtle.exportKey(
      "jwk",
      key
    );
    //alert(exported);
    var jsonString = JSON.stringify(exported);
    //alert(jsonString);
    console.log(jsonString);
}

function encryptMessage(msg, public_key){
    // msg is the text we want to encrypt
    // public_key is the friend who you want to talk to 's public key
    var pub_key = window.importPublicKey(JSON.parse(public_key)); // back to Crypto key object


    var encoded_msg = window.str2ab(msg);
    return crypto.subtle.encrypt(
        {
            name: 'RSA-OAEP'
        },
        pub_key,
        encoded_msg // data that want to encrypt -- should be an array buffer format
    )
    .then(function(encrypted){
        var encrypted_msg = new Uint8Array(encrypted); // return an arraybuffer of the encrypted message
        alert(encrypted_msg);
    })
    .catch(function(err){
        console.log(err);
    })
}

function decryptMessage(encrypted_msg, private_key){
    var pri_key = window.importPrivateKey(JSON.parse(private_key));

    return crypto.subtle.decrypt(
        {
            name: 'RSA-OAEP'
        },
        pri_key,
        encrypted_msg
    )
    .then(function(decrypted){
        var decrypted_msg = new Uint8Array(decrypted);
        // convert decrypted msg back to string
        var str_msg = widow.ab2str(decrypted_msg);
        alert(str_msg)

    })
    .catch(function(err){
        console.log(err);
    })
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


// window.generateKeyPairs();



