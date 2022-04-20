// hash and salt the password
// generate RSA key pairs
// export public key and send it to the server
// export private key and store it locally

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

function generate_SEK(){
    // symmtric key used to sign ? maybe
    // need to generate every time when alice and bob want to talk
    // share between alice and bob ?
    window.crypto.subtle.generateKey(
        {
            name: 'AES-GCM',
            length: 256,
        },
        true,
        ['encrypt', 'decrypt'] // might change to sign
    )
    .then(function(sek){
        console.log(sek);
    })
    .catch(function(err){
        console.log(err);
    })
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
let exported_pri = await window.exportCryptoKey(private_key);


let encrypted_result = await window.encryptMessage("hello",exported_pub);

let decrtpted_result = await window.decryptMessage(encrypted_result, exported_pri);

console.log(decrtpted_result);
console.log(window.ab2str(decrtpted_result));