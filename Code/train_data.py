import pandas as pd
import keras
import numpy as np
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense

# Đọc dữ liệu từ file Excel
excel_file_path = "C:\\Users\\ADMIN\\Documents\\IoT_D20CQCNPM02-N-Nhom32-NguyenGiaVinh-NguyenQuocKhaPhi\\Code\\phising_data20.xlsx"  # Thay đổi đường dẫn tới file Excel của bạn
df = pd.read_excel(excel_file_path)

# Hàm để chuyển đổi URL thành danh sách các ký tự
def url_to_char_list(url):
    return [char for char in url]

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

# In ra từ điển số nguyên ứng với ký tự
char_index = tokenizer.word_index
print("Từ điển số nguyên ứng với ký tự:")
print(char_index)

# Duyệt qua mỗi URL và in ra ma trận số nguyên
for url in X_train:
    url_char_list = url_to_char_list(url)
    url_sequence = tokenizer.texts_to_sequences([url_char_list])[0]
    
    print(f"\nURL: {url}")
    print("Ma trận số nguyên:")
    for char_index in url_sequence:
        print(char_index, end=' ')
    print()

X_train = tokenizer.texts_to_sequences(X_train)
X_train = pad_sequences(X_train)

y_train = np.array(y_train)

# Xây dựng mô hình
model = Sequential()
model.add(Embedding(input_dim=128, output_dim=64, input_length=X_train.shape[1]))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
model.fit(X_train, y_train, epochs=10, batch_size=1)

# Lưu trọng số và cấu trúc mô hình vào một file
model.save("phishing_model20.h5")
print("Model đã được lưu.")

