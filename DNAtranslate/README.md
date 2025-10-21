# DNAtranslate - 浏览器端 DNA→蛋白 翻译与实验小工具

一个纯原生 JavaScript 的前端工具集，提供：
- DNA 序列翻译为氨基酸序列
- 密码子优化（人/大肠杆菌/酵母/昆虫 BEVS/CHO）
- 多肽设计与评分
- 实验计算器（溶液配制、抗体标记、ELISA 稀释表等）

## 使用

在你的页面引入 `translate.js`，并通过相应的 DOM 元素与函数进行交互：
```html
<script src="DNAtranslate/translate.js"></script>
<script>
  // 例如：翻译 DNA 为氨基酸
  document.getElementById('btn').onclick = function () {
    translateDNA();
  }
</script>
```

你可以根据现有的函数 ID（如 dnaSequence、resultAminoAcidSequence 等）构建自己的页面结构，或将函数移植到你的前端工程中。

## 许可证
未明确声明（默认保留）。
