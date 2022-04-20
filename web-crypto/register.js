// hash and salt the password
// generate RSA key pairs
// export public key and send it to the server
// export private key and store it locally

async function hashing(password){
    // passpord is the thing that the user put in
    
}

async function generateKeyPairs() {
    return await window.crypto.subtle.generateKey(
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
        const pubk = window.exportCryptoKey(public_key);
        const prik = window.exportCryptoKey(private_key);
        // store the private key in local
        localStorage.setItem('private key', prik);
        console.log(pubk);
        console.log(prik);

        var encrypted = encryptMessage("hello", pubk);
        window.decryptMessage(encrypted, prik);

    })
    .catch(function(err){
        console.log(err);
    })
}

async function generate_SEK(){
    // symmtric key used to sign ? maybe
    // need to generate every time when alice and bob want to talk
    // share between alice and bob ?
    return await window.crypto.subtle.generateKey(
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
    return await window.crypto.subtle.importKey(
        "jwk",
        jwk,
        {    
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
      true,
      ['encrypt', 'decrypt']
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
            name: 'RSA-OAEP',
            hash: 'SHA-256'
        },
      true,
      ['encrypt','decrypt']
    )
    .then(function(privatekey){
        console.log(privatekey);
    })
    .catch(function(err){
        console.log(err);
    })
  }

async function exportCryptoKey(key) {
    return await window.crypto.subtle.exportKey(
      "jwk",
      key
    )
    .then(function(jwk){
        //alert(exported);
        //var jsonString = JSON.stringify(jwk);
        //alert(jsonString);
        console.log("this is jwk format: ");
        console.log(jwk);
    })
    .catch(function(err){
        console.log(err);
    })
    
}

async function encryptMessage(msg, public_key){
    // msg is the text we want to encrypt
    // public_key is the friend who you want to talk to 's public key
    var pub_key =  window.importPublicKey(public_key); // back to Crypto key object
    
    
    var encoded_msg = window.str2ab(msg);
    return await crypto.subtle.encrypt(
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

async function decryptMessage(encrypted_msg, private_key){
    var pri_key = window.importPrivateKey(private_key);

    return await crypto.subtle.decrypt(
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


window.generateKeyPairs();