# planka-jp

[Planka](https://github.com/plankanban/planka)（Trello代替のカンバンOSS・PLANKA Community License）を日本語で使うための補助リポジトリです。

- `i18n/ja-JP.additions.json` — 公式dockerイメージ(2026-09時点)の `ja-JP/core.js` に無かった **56キー**の日本語訳（自動ログアウト・2要素認証・認証系）。`{{name}}` 等のプレースホルダは原文と同一であることを検証済み
- `scripts/merge_ja.py` — 本家 `client/src/locales/ja-JP/core.js` に追記するスクリプト（`node --check` で構文確認済み）
- `docker-compose.example.yml` — 公式構成に差し替え箇所（BASE_URL / SECRET_KEY / 初期管理者）を明示したもの

本家への翻訳提案は、Planka が受け付けているプルリクエストで行います。取り込まれた後は、このパッチは不要になります。

## 使い方

```bash
git clone https://github.com/katsushi2441/planka-jp.git && cd planka-jp
cp docker-compose.example.yml docker-compose.yml   # BASE_URL / SECRET_KEY / DEFAULT_ADMIN_* を自分の値に
docker compose up -d
```

翻訳をソースに組み込む場合:

```bash
python3 scripts/merge_ja.py /path/to/planka/client/src/locales/ja-JP/core.js
```

## 落とし穴（実測）

- `BASE_URL` が実際に開くURLと違うと、ログインは通るのに画面が真っ白になります（別オリジン扱いで無音停止）
- `DEFAULT_ADMIN_*` の値に空白を入れるとログインできません
- 初回ログインは利用規約への同意が必要。APIからは `POST /api/access-tokens`(403+pendingToken) → `GET /api/terms`(signature) → `POST /api/access-tokens/accept-terms`

## 解説記事

- https://katsushi2441.github.io/vwork/articles/2026-09-04-planka-japanese-guide.html

## ライセンス

Planka 本体は PLANKA Community License v1.1（自社内利用・自社ホスティングは無償。第三者向けホスティングは商用ライセンスが必要）。本リポジトリの翻訳・スクリプトは MIT で提供します。
