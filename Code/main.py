from flask import Flask, request, jsonify
from flask_cors import CORS
import keras
import pandas as pd
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences

app = Flask(__name__)
CORS(app)

# Hàm để chuyển đổi URL thành danh sách các ký tự
def url_to_char_list(url):
    return [char for char in url]

tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)

# Đọc dữ liệu từ file Excel
excel_file_path = "C:\\Users\\ADMIN\\Documents\\IoT_D20CQCNPM02-N-Nhom32-NguyenGiaVinh-NguyenQuocKhaPhi\\Code\\phising_data20.xlsx"  # Thay đổi đường dẫn tới file Excel của bạn
df = pd.read_excel(excel_file_path)

# Ánh xạ nhãn thành số: "trusted" -> 1, "phishing" -> 0
df['label'] = df['label'].map({'trusted': 1, 'phishing': 0})

# Chuyển đổi URL thành danh sách các ký tự
df['char_list'] = df['url'].apply(url_to_char_list)

# Tạo tập dữ liệu đào tạo
X_train = df['char_list'].tolist()
y_train = df['label'].tolist()

# Chuyển đổi URL thành vectơ số nguyên để đưa vào mô hình
tokenizer = keras.preprocessing.text.Tokenizer(char_level=True)
tokenizer.fit_on_texts(X_train)
X_train = tokenizer.texts_to_sequences(X_train)
X_train = pad_sequences(X_train)

# Tải lại mô hình từ file
loaded_model = load_model("C:\\Users\\ADMIN\\Documents\\IoT_D20CQCNPM02-N-Nhom32-NguyenGiaVinh-NguyenQuocKhaPhi\\Code\\phishing_model20.h5")
print("Mô hình đã được tải lại.")

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    # Kiểm tra xem yêu cầu có chứa dữ liệu JSON không
    if request.is_json:
        data = request.get_json()

        # Kiểm tra xem dữ liệu JSON có chứa key 'url' không
        if 'url' in data:
            new_url = data['url']
            print(data['url'])

            url_char_list = url_to_char_list(new_url)
            url_sequence = tokenizer.texts_to_sequences([url_char_list])[0]
            
            print(f"\nURL: {url_char_list}")
            print("Ma trận số nguyên:")
            for char_index in url_sequence:
                print(char_index, end=' ')
            print()

            new_char_list = url_to_char_list(new_url)
            X_new = tokenizer.texts_to_sequences([new_char_list])
            X_new = pad_sequences(X_new, maxlen=X_train.shape[1])

            # Đưa ra dự đoán với mô hình đã tải lại
            prediction = loaded_model.predict(X_new)
            confidence = prediction[0, 0]

            # Chuyển đổi kết quả dự đoán thành văn bản
            if confidence > 0.5:
                result1 = "URL đáng tin cậy"
                result2 = 1
            else:
                result1 = "URL có khả năng phishing"
                result2 = 0
            print(prediction)
            return jsonify({'result1': result1, 'result2': result2})

    # Trả về lỗi nếu không tìm thấy dữ liệu JSON hoặc key 'url'
    return jsonify({'error': 'Invalid JSON data'}), 400


if __name__ == '__main__':
    app.run(debug=True)