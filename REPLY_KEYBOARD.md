# 📱 SoNoBot - Reply Keyboard Guide

## 🎯 Reply Keyboard Features

SoNoBot现已支持 **Reply Keyboard**，让用户可以更方便地使用所有功能！

## 🔘 Nút bấm có sẵn

### Chính:
- **💰 NẠP tiền** - Mở hướng dẫn NẠP tiền
- **💸 RÚT tiền** - Mở hướng dẫn RÚT tiền  
- **📊 Xem báo cáo** - Hiển thị báo cáo công nợ
- **🗑️ Xóa giao dịch** - Mở hướng dẫn xóa giao dịch

### Phụ:
- **❓ Hướng dẫn** - Hiển thị hướng dẫn chi tiết
- **⚙️ Menu chính** - Hiển thị menu tổng quan

## 🎮 Cách sử dụng

### 1. Bắt đầu
```bash
/start
```
Bot sẽ hiển thị Reply Keyboard với các nút bấm.

### 2. Sử dụng nút bấm
Chỉ cần nhấn vào nút tương ứng:
- Nhấn **💰 NẠP tiền** → Bot hiển thị cú pháp NẠP tiền
- Nhấn **💸 RÚT tiền** → Bot hiển thị cú pháp RÚT tiền
- Nhấn **📊 Xem báo cáo** → Bot hiển thị báo cáo công nợ
- Nhấn **🗑️ Xóa giao dịch** → Bot hiển thị hướng dẫn xóa

### 3. Kết hợp nút và lệnh
Bạn có thể:
- Dùng nút để xem hướng dẫn
- Gõ lệnh trực tiếp để thực thi nhanh

## 📝 Ví dụ thực tế

### NẠP tiền (ghi nợ bạn cafe):
1. Nhấn **💰 NẠP tiền**
2. Nhìn cú pháp: `/no @user [số tiền] [lý do]`
3. Gõ: `/no @friend 50k cafe`

### Kiểm tra công nợ:
1. Nhấn **📊 Xem báo cáo**
2. Bot hiển thị báo cáo chi tiết

### Xem menu:
1. Nhấn **⚙️ Menu chính**
2. Xem tất cả chức năng

## 🎨 Lợi ích Reply Keyboard

✅ **Tiện lợi** - Không cần nhớ lệnh
✅ **Nhanh chóng** - Chạm để thực hiện  
✅ **Trực quan** - Giao diện thân thiện
✅ **Linh hoạt** - Kết hợp nút và lệnh

## 🔧 Technical Implementation

Reply Keyboard được implement với:

```python
reply_markup = {
    "keyboard": [
        [{"text": "💰 NẠP tiền"}],
        [{"text": "💸 RÚT tiền"}],
        [{"text": "📊 Xem báo cáo"}],
        [{"text": "🗑️ Xóa giao dịch"}, {"text": "⚙️ Menu chính"}]
    ],
    "resize_keyboard": True,
    "one_time_keyboard": False
}
```

## 🎯 Tương lai

Kế hoạch phát triển Reply Keyboard:
- [ ] Inline Keyboard cho các lựa chọn nhanh
- [ ] Dynamic buttons dựa trên trạng thái
- [ ] Multi-language support
- [ ] Custom themes

---

**SoNoBot** - Quản lý nợ chưa bao giờ dễ dàng hơn! 💰📊