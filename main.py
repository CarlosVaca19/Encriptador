from cryptography.fernet import Fernet, InvalidToken
from flask import Flask, render_template, request
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        fernet_key = request.form['key'].encode()  # Obtener la clave en texto plano
        
        # Codificar la clave en base64
        fernet_key = base64.urlsafe_b64encode(fernet_key)
        
        # Asegurarse de que la clave sea de 32 bytes
        if len(fernet_key) != 44:
            return 'La clave debe tener 32 caracteres'
        
        fernet = Fernet(fernet_key)
        
        if 'file' in request.files:
            file = request.files['file']
            
            # Verificar si se seleccionó un archivo
            if file.filename != '':
                file.save(file.filename)
                
                if 'encrypt' in request.form:
                    encrypted_file_path = encrypt_file(file.filename, fernet)
                    return f'Archivo encriptado guardado como: {encrypted_file_path}'
                
                if 'decrypt' in request.form:
                    decrypted_file_path = decrypt_file(file.filename, fernet)
                    return f'Archivo desencriptado guardado como: {decrypted_file_path}'
        
    return render_template('index.html')

def encrypt_file(file_path, fernet):
    with open(file_path, 'rb') as file:
        data = file.read()
        
    encrypted_data = fernet.encrypt(data)
    
    encrypted_file_path = f'{file_path}.encrypted'
    
    with open(encrypted_file_path, 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    
    return encrypted_file_path

def decrypt_file(file_path, fernet):
    with open(file_path, 'rb') as file:
        data = file.read()
        
    decrypted_data = fernet.decrypt(data)
    
    decrypted_file_path = file_path.replace('.encrypted', '.decrypted')
    
    with open(decrypted_file_path, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    
    return decrypted_file_path

if __name__ == '__main__':
    app.run(debug=True)
