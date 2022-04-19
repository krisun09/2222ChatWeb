(() => {

    /*
    Store the calculated ciphertext here, so we can decrypt the message later.
    */
    let ciphertext;

    /*
    Generate an encryption key pair, then set up event listeners
    on the "Encrypt" and "Decrypt" buttons.
    */
    
    
    var keypair = window.crypto.subtle.generateKey(
        {
            name: "RSA-OAEP",
            modulusLength: 2048,
            publicExponent: new Uint8Array([1, 0, 1]),
            hash: "SHA-256",
        },
        true, // whether the key is extractable (i.e. can be used in exportKey)
        ["encrypt", "decrypt"]
    )
    .then(function(key){
        // 如果成功，执行这个function
        //returns a keypair object
        var public_key = key.publicKey;
        var private_key = key.privateKey;
        

    })
    .catch(function(err){
        // 如果不成功，执行这个函数
        console.error(err);
    });
    
    
    
    
    /*
    Fetch the contents of the "message" textbox, and encode it
    in a form we can use for the encrypt operation.
    */
    function getMessageEncoding(key) {
        // fetch the firat "#rsa-oaep-message" element within the document
        const messageBox = document.querySelector("#rsa-oaep-message");
        let message = messageBox.value;
        // generate a byte stream with UTF-8 encoding
        let enc = new TextEncoder();
        return enc.encode(message);
    }

    /*
    Get the encoded message, encrypt it and display a representation 
    of the ciphertext in the "Ciphertext" element.
    */
    async function encryptMessage(key) {
        let encoded = getMessageEncoding();
        ciphertext = await window.crypto.subtle.encrypt(
            {
                name: "RSA-OAEP"
            },
            key,
            encoded
        );

        let buffer = new Uint8Array(ciphertext, 0, 5);
        const ciphertextValue = document.querySelector(".rsa-oaep .ciphertext-value");
    }

    /*
    Fetch the ciphertext and decrypt it.
    Write the decrypted message into the "Decrypted" box.
    */
    async function decryptMessage(key) {
        let decrypted = await window.crypto.subtle.decrypt(
        {
            name: "RSA-OAEP"
        },
        key,
        ciphertext
        );

        let dec = new TextDecoder();
        const decryptedValue = document.querySelector(".rsa-oaep .decrypted-value");
        decryptedValue.textContent = dec.decode(decrypted);
    }

})();