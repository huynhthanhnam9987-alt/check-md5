#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script tạo tài khoản ChatGPT hàng loạt
Hỗ trợ tạo nhiều tài khoản cùng lúc với các thông tin khác nhau
"""

import asyncio
import json
import random
import string
import time
from datetime import datetime
from pathlib import Path
import requests
from typing import List, Dict, Tuple


class TaoEmailNgauNhien:
    """Tạo email độc nhất cho từng tài khoản"""
    
    def __init__(self, mien_email: str = "example.com"):
        self.mien_email = mien_email
        self.danh_sach_email_da_dung = set()
    
    def tao_email(self) -> str:
        """Sinh email ngẫu nhiên độc nhất"""
        while True:
            # Tạo phần ngẫu nhiên từ chữ và số
            phan_ngau_nhien = ''.join(random.choices(
                string.ascii_lowercase + string.digits, 
                k=12
            ))
            # Thêm timestamp để đảm bảo độc nhất
            timestamp = int(time.time() * 1000) % 10000
            email = f"user_{phan_ngau_nhien}_{timestamp}@{self.mien_email}"
            
            if email not in self.danh_sach_email_da_dung:
                self.danh_sach_email_da_dung.add(email)
                return email


class TaoMatKhauAnToan:
    """Tạo mật khẩu an toàn cho tài khoản"""
    
    @staticmethod
    def tao_mat_khau(chieu_dai: int = 16) -> str:
        """
        Tạo mật khẩu ngẫu nhiên an toàn
        - Chứa chữ hoa, chữ thường, số và ký tự đặc biệt
        """
        ky_tu_chu_hoa = string.ascii_uppercase
        ky_tu_chu_thuong = string.ascii_lowercase
        ky_tu_so = string.digits
        ky_tu_dac_biet = "!@#$%^&*_+-="
        
        # Đảm bảo có ít nhất một ký tự từ mỗi loại
        mat_khau = [
            random.choice(ky_tu_chu_hoa),
            random.choice(ky_tu_chu_thuong),
            random.choice(ky_tu_so),
            random.choice(ky_tu_dac_biet)
        ]
        
        # Điền phần còn lại với ký tự ngẫu nhiên
        tat_ca_ky_tu = ky_tu_chu_hoa + ky_tu_chu_thuong + ky_tu_so + ky_tu_dac_biet
        mat_khau += random.choices(tat_ca_ky_tu, k=chieu_dai - 4)
        
        # Trộn lẫn thứ tự
        random.shuffle(mat_khau)
        return ''.join(mat_khau)


class TaoBanGhiChiTiet:
    """Ghi lại chi tiết quá trình tạo tài khoản"""
    
    def __init__(self, ten_file: str = "ban_ghi_tao_tai_khoan.txt"):
        self.ten_file = ten_file
        self.duong_dan = Path(ten_file)
    
    def ghi_log(self, thong_bao: str, loai: str = "INFO"):
        """Ghi log vào file và console"""
        thoigian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        thong_bao_day_du = f"[{thoigian}] [{loai}] {thong_bao}"
        
        print(thong_bao_day_du)
        
        with open(self.duong_dan, 'a', encoding='utf-8') as f:
            f.write(thong_bao_day_du + "\n")
    
    def xoa_file_cu(self):
        """Xóa file log cũ"""
        if self.duong_dan.exists():
            self.duong_dan.unlink()


class TaoTaiKhoanHangLoat:
    """Quản lý tạo hàng loạt tài khoản ChatGPT"""
    
    def __init__(self, 
                 url_api: str = "https://api.openai.com/v1/auth/signup",
                 khoa_api: str = "YOUR_API_KEY",
                 mien_email: str = "example.com"):
        """
        Khởi tạo hệ thống tạo tài khoản
        
        Args:
            url_api: URL endpoint API để tạo tài khoản
            khoa_api: API key xác thực
            mien_email: Miền email sử dụng
        """
        self.url_api = url_api
        self.khoa_api = khoa_api
        self.mien_email = mien_email
        
        self.tao_email = TaoEmailNgauNhien(mien_email)
        self.tao_mat_khau = TaoMatKhauAnToan()
        self.ban_ghi = TaoBanGhiChiTiet()
        
        self.danh_sach_tai_khoan_thanh_cong = []
        self.danh_sach_tai_khoan_that_bai = []
        
        self.ban_ghi.xoa_file_cu()
        self.ban_ghi.ghi_log("=" * 60)
        self.ban_ghi.ghi_log("BẮT ĐẦU CHƯƠNG TRÌNH TẠO TÀI KHOẢN CHATGPT HÀNG LOẠT")
        self.ban_ghi.ghi_log("=" * 60)
    
    def tao_thong_tin_tai_khoan(self, so_thu_tu: int) -> Dict:
        """Tạo thông tin cấu hình cho một tài khoản"""
        email = self.tao_email.tao_email()
        mat_khau = self.tao_mat_khau.tao_mat_khau()
        
        thong_tin = {
            "so_thu_tu": so_thu_tu,
            "email": email,
            "mat_khau": mat_khau,
            "ten_hien_thi": f"User_{so_thu_tu}",
            "thoi_gian_tao": datetime.now().isoformat(),
            "trang_thai": "chưa_tạo"
        }
        
        return thong_tin
    
    def tao_danh_sach_tai_khoan(self, so_luong: int) -> List[Dict]:
        """Tạo danh sách cấu hình N tài khoản"""
        self.ban_ghi.ghi_log(f"Đang tạo cấu hình cho {so_luong} tài khoản...", "INFO")
        
        danh_sach = []
        for i in range(1, so_luong + 1):
            thong_tin = self.tao_thong_tin_tai_khoan(i)
            danh_sach.append(thong_tin)
        
        self.ban_ghi.ghi_log(f"Đã tạo cấu hình cho {so_luong} tài khoản", "THANH_CÔNG")
        return danh_sach
    
    async def tao_tai_khoan_tuy_le(self, thong_tin_tai_khoan: Dict) -> Tuple[bool, str]:
        """
        Tạo một tài khoản duy nhất
        
        Returns:
            Tuple[bool, str]: (thành công hay không, thông báo)
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.khoa_api}",
                "Content-Type": "application/json"
            }
            
            du_lieu = {
                "email": thong_tin_tai_khoan["email"],
                "password": thong_tin_tai_khoan["mat_khau"],
                "display_name": thong_tin_tai_khoan["ten_hien_thi"]
            }
            
            # Simulate API call (thay bằng requests.post thực tế)
            await asyncio.sleep(random.uniform(0.5, 1.5))  # Giả lập độ trễ mạng
            
            # Trong thực tế, bạn sẽ gọi:
            # response = requests.post(self.url_api, headers=headers, json=du_lieu, timeout=10)
            
            # Giả lập phản hồi thành công
            if random.random() > 0.1:  # 90% thành công
                thong_tin_tai_khoan["trang_thai"] = "tạo_thành_công"
                self.danh_sach_tai_khoan_thanh_cong.append(thong_tin_tai_khoan)
                return True, f"Tài khoản {thong_tin_tai_khoan['email']} tạo thành công"
            else:
                raise Exception("Lỗi từ API")
        
        except Exception as loi:
            thong_tin_tai_khoan["trang_thai"] = "tạo_thất_bại"
            thong_tin_tai_khoan["loi"] = str(loi)
            self.danh_sach_tai_khoan_that_bai.append(thong_tin_tai_khoan)
            return False, f"Lỗi: {str(loi)}"
    
    async def tao_hang_loat(self, danh_sach_tai_khoan: List[Dict], 
                           so_ket_noi_dong_thoi: int = 5) -> None:
        """
        Tạo hàng loạt tài khoản với giới hạn kết nối đồng thời
        
        Args:
            danh_sach_tai_khoan: Danh sách thông tin tài khoản
            so_ket_noi_dong_thoi: Số kết nối được phép cùng một lúc
        """
        self.ban_ghi.ghi_log(
            f"Bắt đầu tạo {len(danh_sach_tai_khoan)} tài khoản "
            f"(tối đa {so_ket_noi_dong_thoi} kết nối cùng lúc)", 
            "INFO"
        )
        
        semaphore = asyncio.Semaphore(so_ket_noi_dong_thoi)
        
        async def tao_voi_gioi_han(tai_khoan):
            async with semaphore:
                thanh_cong, thong_bao = await self.tao_tai_khoan_tuy_le(tai_khoan)
                loai_log = "THANH_CÔNG" if thanh_cong else "THẤT_BẠI"
                self.ban_ghi.ghi_log(thong_bao, loai_log)
        
        # Tạo tất cả task không đồng bộ
        cac_task = [tao_voi_gioi_han(tai_khoan) for tai_khoan in danh_sach_tai_khoan]
        
        # Chờ tất cả task hoàn thành
        await asyncio.gather(*cac_task)
        
        # Ghi tóm tắt kết quả
        self._ghi_tom_tat_ket_qua()
    
    def _ghi_tom_tat_ket_qua(self) -> None:
        """Ghi tóm tắt kết quả tạo tài khoản"""
        self.ban_ghi.ghi_log("\n" + "=" * 60, "INFO")
        self.ban_ghi.ghi_log("TÓM TẮT KẾT QUẢ", "INFO")
        self.ban_ghi.ghi_log("=" * 60, "INFO")
        self.ban_ghi.ghi_log(
            f"Tổng tài khoản thành công: {len(self.danh_sach_tai_khoan_thanh_cong)}", 
            "THANH_CÔNG"
        )
        self.ban_ghi.ghi_log(
            f"Tổng tài khoản thất bại: {len(self.danh_sach_tai_khoan_that_bai)}", 
            "THẤT_BẠI"
        )
        self.ban_ghi.ghi_log(
            f"Tỷ lệ thành công: {len(self.danh_sach_tai_khoan_thanh_cong) / "
            f"(len(self.danh_sach_tai_khoan_thanh_cong) + len(self.danh_sach_tai_khoan_that_bai)) * 100:.2f}%",
            "INFO"
        )
    
    def luu_thong_tin_tai_khoan(self, ten_file: str = "tai_khoan_chatgpt.json") -> None:
        """Lưu thông tin tài khoản vào file JSON"""
        du_lieu_luu = {
            "thoi_gian_tao": datetime.now().isoformat(),
            "tong_thanh_cong": len(self.danh_sach_tai_khoan_thanh_cong),
            "tong_that_bai": len(self.danh_sach_tai_khoan_that_bai),
            "tai_khoan_thanh_cong": self.danh_sach_tai_khoan_thanh_cong,
            "tai_khoan_that_bai": self.danh_sach_tai_khoan_that_bai
        }
        
        with open(ten_file, 'w', encoding='utf-8') as f:
            json.dump(du_lieu_luu, f, ensure_ascii=False, indent=2)
        
        self.ban_ghi.ghi_log(f"Đã lưu thông tin tài khoản vào file: {ten_file}", "INFO")


async def main():
    """Hàm chính"""
    print("\n" + "="*60)
    print("CHƯƠNG TRÌNH TẠO TÀI KHOẢN CHATGPT HÀNG LOẠT")
    print("="*60 + "\n")
    
    # Cấu hình
    SO_LUONG_TAI_KHOAN = 10  # Số lượng tài khoản muốn tạo
    SO_KET_NOI_DONG_THOI = 3  # Số kết nối được phép cùng một lúc
    MIEN_EMAIL = "example.com"  # Miền email
    
    # Tạo đối tượng quản lý
    tao_tai_khoan = TaoTaiKhoanHangLoat(mien_email=MIEN_EMAIL)
    
    # Tạo danh sách thông tin tài khoản
    danh_sach = tao_tai_khoan.tao_danh_sach_tai_khoan(SO_LUONG_TAI_KHOAN)
    
    # Tạo hàng loạt tài khoản
    await tao_tai_khoan.tao_hang_loat(danh_sach, so_ket_noi_dong_thoi=SO_KET_NOI_DONG_THOI)
    
    # Lưu thông tin tài khoản
    tao_tai_khoan.luu_thong_tin_tai_khoan()
    
    print("\n✅ Hoàn thành! Kiểm tra file 'tai_khoan_chatgpt.json' để xem kết quả\n")


if __name__ == "__main__":
    asyncio.run(main())
