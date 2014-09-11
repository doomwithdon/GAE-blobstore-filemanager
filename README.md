版本:0.0.0.2
============
<h2>
版本維護日誌</h2>
<h2>
一、New</h2>
<div>
<ol>
<li>為使用者上傳總攬情形添加表格</li>
<li>添增webapp.template.register_template_library('filterdir.customfilters')，客製化模板語言的filter</li>
</ol>
</div>

<h2>
二、Debug</h2>
<div>
<ol>
<li><span style="color: #333333; font-family: Consolas, 'Liberation Mono', Menlo, Courier, monospace; font-size: 15px; white-space: pre-wrap;">django的filter函數要與|相鄰，範例如下</span></li>
</ol>
<ul>
<li style="font-size: 15px; white-space: pre-wrap;"><span style="color: #333333; font-family: Consolas, 'Liberation Mono', Menlo, Courier, monospace;">{{ wrapper.blob.size|countByte }} is O</span></li>
<li style="font-size: 15px; white-space: pre-wrap;"><span style="color: #333333; font-family: Consolas, 'Liberation Mono', Menlo, Courier, monospace;">{{ wrapper.blob.size| countByte }} is X</span></li>
</ul>
<div>
<span style="color: #333333; font-family: Consolas, Liberation Mono, Menlo, Courier, monospace;"><span style="font-size: 15px; white-space: pre-wrap;">
</span></span></div>
</div>
</div>
</div>
