from flask import Flask, render_template, request, send_file
import os
import tempfile

app = Flask(__name__)

# =========================
# 解の公式の4乗
# =========================

def formula_power4(a, b, c):
    """
    解の公式

        (-b ± √(b² - 4ac)) / 2a

    で求めた2つの解を、それぞれ4乗する。
    """

    discriminant = b ** 2 - 4 * a * c

    if discriminant < 0:
        raise ValueError("実数解が存在しません")

    x1 = (-b + discriminant ** 0.5) / (2 * a)
    x2 = (-b - discriminant ** 0.5) / (2 * a)

    return x1 ** 4, x2 ** 4

# =========================
# ファイル暗号化
# =========================

def encrypt_bytes(data):
    """
    ファイルのバイト列を独自方式で変換する。
    現段階ではテスト用の変換。
    """

    result = bytearray()

    for byte in data:
        # ここに後で「解の公式の4乗」を組み込む
        value = (byte + 7) % 256

        result.append(value)

    return bytes(result)
# =========================
# メイン画面
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# =========================
# 公式テスト
# =========================

@app.route("/formula", methods=["POST"])# =========================
# ファイル暗号化API
# =========================

@app.route("/encrypt", methods=["POST"])
def encrypt_file():

    if "file" not in request.files:
        return {
            "success": False,
            "error": "ファイルがありません"
        }, 400

    file = request.files["file"]

    if file.filename == "":
        return {
            "success": False,
            "error": "ファイルが選択されていません"
        }, 400

    data = file.read()

    encrypted_data = encrypt_bytes(data)

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".encrypted"
    )

    temp_file.write(encrypted_data)
    temp_file.close()

    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name=file.filename + ".encrypted"
    )
def formula_test():

    try:
        a = float(request.form["a"])
        b = float(request.form["b"])
        c = float(request.form["c"])

        result1, result2 = formula_power4(a, b, c)

        return {
            "success": True,
            "result1": result1,
            "result2": result2
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }, 400


# =========================
# アプリ起動
# =========================

if __name__ == "__main__":
    app.run(debug=True)