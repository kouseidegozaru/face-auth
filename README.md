# Face Auth
このアプリケーションでは顔認証を行うための機能を REST API で提供します。

### 機能
 - 画像データの登録
 - 画像データのグループの管理
 - 画像データから推論を行うための特徴モデルの作成
 - 特徴モデルから画像がどの人物かを推論する機能
 - ユーザー認証機能

### エンドポイント
APIのエンドポイントについては以下に記載しています。

[Swagger UI](https://kouseidegozaru.github.io/face-auth/dist/index.html)


### 開発環境
 - Python 3.10.6
 - Django 5.0.7
 - Django allauth 0.63.6
 - Django Rest Framework 3.15.2
 - dj-rest-auth 6.0.0
 - scikit-learn 1.5.2
 - Numpy 1.26.4
 - Dlib 19.22.99
 - cmake 3.28.3
<br>・・・

## 環境構築
1. リポジトリをcloneする
   ```
   git clone https://github.com/kouseidegozaru/face-auth.git
   cd face-auth
   ```
2. 仮想環境の作成とアクティベート
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. cmakeのインストールとビルド

   cmakeの3.28.3をお使いの環境に合わせてインストールしてください

5. dlibのインストール
   
   dlibのwhlをダウンロードし`./venv/`直下に配置してください
   ```
   https://github.com/z-mahmud22/Dlib_Windows_Python3.x/blob/main/dlib-19.22.99-cp310-cp310-win_amd64.whl
   ```

7. ライブラリのインストール
   ```
   pip install -r requirements.txt
   pip install ./venv/dlib-19.22.99-cp310-cp310-win_amd64.whl
   ```

6. envファイルの作成
   `.face_auth/`に`.env`ファイルを作成して次の内容を入力してください
   ```
   DEBUG=on
   SECRET_KEY=yourdjangosecretkey
   ALLOWED_HOSTS=localhost,127.0.0.1,yourallowedhosts
   FRONTEND_URL=http://localhost:3000
   
   CORS_ALLOWED_ORIGINS=http://localhost:3000,yourallowedhosts
   CSRF_TRUSTED_ORIGINS=http://localhost:3000,yourallowedhosts
   SESSION_COOKIE_SECURE=on

   DEFAULT_FROM_EMAIL=youremailaddress
   EMAIL_HOST=youremailhost
   EMAIL_PORT=youremailport
   EMAIL_HOST_USER=youremailaddress
   EMAIL_HOST_PASSWORD=yourhostpassword
   EMAIL_USE_TLS=on
   ```

### 備考
このアプリケーションはバックエンドとして使用することを想定しています。
