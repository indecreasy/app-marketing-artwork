# App 宣传图排版 Skill

从真实产品截图出发，按要传达的内容为每张图选构图，再按渠道完成排版和验收。适合要制作多语言 App Store 物料、朋友圈竖图和微信群长图的开发者。

## 在 Codex 中使用

```sh
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/indecreasy/app-marketing-artwork.git "${CODEX_HOME:-$HOME/.codex}/skills/app-marketing-artwork"
```

提供截图、品牌素材和目标渠道，然后在 Codex 中调用：

> 用 $app-marketing-artwork 把这组 App 截图做成 App Store 宣传图。先告诉我每张图讲什么，以及还需要补拍哪些画面。

[查看 Skill 说明](SKILL.md) · [App Store 指南](references/app-store.md) · [微信指南](references/wechat.md)

## 裁切预览

可用附带的脚本并排查看原图、安全区框线和裁切结果。需要 Python 和 Pillow。

```sh
python3 scripts/preview-crop.py poster.png preview.png --square --preview-width 360
```
