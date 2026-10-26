# THE SNOW CHRISTMAS

2026年12月19・20日、MEGURO MARC のイベントサイト。静的HTMLを配信し、必要な操作と演出だけをJavaScriptで追加します。Storybookやブラウザー向けフレームワークは使用しません。

## 開発と確認

Node.js 22以上、Python 3.10以上が必要です。

```sh
npm ci --ignore-scripts
npm run build
npm run dev
```

開発URL: http://127.0.0.1:3000/ 。同じポートのサーバーが起動済みなら再起動は不要です。

```sh
npm run format
npm run build
npm run format:check
npm test
npm run check
```

ルートの5つのHTMLと `config/event.js` は生成物です。**HTMLを変更する場合は `templates/pages/` または `partials/` を編集して再生成**してください。生成物も配信に必要なので一緒に管理します。`scripts/sync-shell.py` は既存手順との互換用で、現在は全体ビルドを呼びます。

## 編集元

| 変更 | 編集元 |
| --- | --- |
| 本文・各ページの構造 | `templates/pages/*.html` |
| 共通ヘッダー・フッター | `partials/header.html`, `partials/footer.html` |
| ガーランドSVG | `partials/garland.html` |
| 開催日・会場・共有URL・寄付リンク | `config/event.json` |
| 基本文字・基本レイアウト | `style.css` |
| ヘッダーの完成スタイル | `snow-header.css` |
| 共通フッター・ボタンの形 | `site-shell.css` |
| トップ、雪の装飾、People、予定 | `snow-lp.css`, `snow-world.css`, `people.css`, `calendar.css` |
| 雪募金・お礼ページ固有 | `snowfund.css`, `snowfund-thanks.css` |

日付設定は見出し・ヘッダー・共有文・Googleカレンダー・ICSに反映されます。装飾カレンダーの前後週のマス、告知文の予定月、イルミネーション期間は別の編集情報です。開催日を変更した場合はそれらも確認してください。開場時間は未確定のため終日予定です。

## 品質管理

- `npm run check`: 再生成漏れ、ローカルリンク・アンカー切れ、ID重複、画像alt、CSS/JS構文、承認済み本文、容量上限を検査。
- `npm test`: 終日予定の終了日、月末繰り上がり、テンプレート誤記、キャッシュ更新等の回帰テスト。
- `.github/workflows/quality.yml`: PR/push時に同じ検査を実行する定義。デプロイ処理は含みません。
- `tests/content-baseline.json`: 今回の整理前の本文。文言を意図的に変更するときは差分確認後に更新します。チェックを通す目的だけで更新しないでください。
- CSS/JSのURLには内容から生成したハッシュを付与します。手動で `?v=...` を増やす必要はありません。

詳細: [構造](docs/architecture.md) / [素材](docs/assets.md) / [公開手順](docs/release.md) / [今回の検証](docs/refactor-report.md)。
