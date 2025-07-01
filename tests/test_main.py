import pytest
import tempfile
from pathlib import Path
import os
import sys
import main

@pytest.fixture(autouse=True)
def cleanup_qr_file():
    # Cleanup any test files created
    yield
    for f in Path('.').glob('test_qr_*.png'):
        try:
            f.unlink()
        except Exception:
            pass

def test_generate_qr_code_valid_url_creates_file(monkeypatch):
    # Arrange
    url = "https://example.com"
    temp_path = Path(f"test_qr_valid.png")
    # Patch is_valid_url to always return True for this test
    monkeypatch.setattr(main, "is_valid_url", lambda x: True)
    # Act
    main.generate_qr_code(url, temp_path, fill_color='blue', back_color='yellow')
    # Assert
    assert temp_path.exists()
    temp_path.unlink()

def test_generate_qr_code_invalid_url_does_not_create_file(monkeypatch):
    url = "not_a_valid_url"
    temp_path = Path(f"test_qr_invalid.png")
    monkeypatch.setattr(main, "is_valid_url", lambda x: False)
    main.generate_qr_code(url, temp_path)
    assert not temp_path.exists()

def test_generate_qr_code_handles_exceptions(monkeypatch):
    url = "https://example.com"
    temp_path = Path(f"test_qr_exception.png")
    monkeypatch.setattr(main, "is_valid_url", lambda x: True)
    # Patch qrcode.QRCode to raise an exception
    class DummyQRCode:
        def __init__(*a, **k): pass
        def add_data(*a, **k): raise Exception("QR error")
        def make(*a, **k): pass
        def make_image(*a, **k): pass
    monkeypatch.setattr(main.qrcode, "QRCode", DummyQRCode)
    # Should not raise, just log error
    main.generate_qr_code(url, temp_path)
    assert not temp_path.exists()