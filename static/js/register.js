// hash and salt the password
// generate RSA key pairs
// export public key and send it to the server
// export private key and store it locally


function generateKeyPairs() {
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
        var prik = window.exportCryptoKey(private_key);

    })
    .catch(function(err){
        console.log(err);
    })
}

function generate_SEK(){
    // symmtric key used to sign ? maybe
    // need to generate every time when alice and bob want to talk
    // share between alice and bob ?
    return crypto.subtle.generateKey(
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

async function importCryptoKey(jwk){
    

}

async function exportCryptoKey(key) {
    const exported = await window.crypto.subtle.exportKey(
      "jwk",
      key
    );
    alert(exported);
    var jsonString = JSON.stringify(exported);
    alert(jsonString);
    console.log(jsonString);
    return jsonString;
}


window.generateKeyPairs() 

