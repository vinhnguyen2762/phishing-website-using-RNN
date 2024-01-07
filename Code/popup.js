document.addEventListener('DOMContentLoaded', function() {
    
    // Hàm lấy địa chỉ URL hiện tại của tab
    function getCurrentTabURL(callback) {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        var currentURL = "";
        var currentTab = tabs[0];
        currentURL = currentTab.url;
        callback(currentURL);
    });
    }

    getCurrentTabURL((url) => {callApi(url)})
    // Gọi API khi trang web popup được tải
    

    function callApi(url) {
        // Gọi API từ đường dẫn API của bạn
        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                'url': 'http://br-icloud.com.br' // Thay đổi thành URL bạn muốn dự đoán
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response data:', data);
            // Hiển thị kết quả trên trang web popup
            displayResult(data.result1, data.result2);
        })
        .catch(error => {
            console.error('Error calling API:', error);
        });
    }
    

    function displayResult(result1, result2) {
        // Cập nhật nội dung HTML của popup với kết quả
        document.getElementById('status').innerText = result1;
        document.getElementById('image-result').src = result2 == 0
            ? 'phishing.png'  // Đường dẫn đến hình ảnh cho URL đáng tin cậy
            : 'trusted.png'; // Đường dẫn đến hình ảnh cho URL có khả năng phishing
        document.getElementById('image-result').hidden = false;
    }
});
