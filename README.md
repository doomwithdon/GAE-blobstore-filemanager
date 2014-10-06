版本:0.2.0.0
=============
<h2>
版本維護日誌</h2>
<h2>
一、New</h2>
<div>
<ol>
<li>DashBoard，新增 Google API 的 Chart 功能</li>
<li>新增 &nbsp;GAE 的 Cron 工作排程設定，可以定時重置流量</li>
</ol>
<div>

</div>
</div>
<div>
<h2>
二、Optimization</h2>
</div>
<div>
<ul>
<li>DashBoard網頁服務</li>
</ul>
</div>
<div>
<ol>
<li>&nbsp;DashBoard的Chart，擁有"圖表大小調整"功能，無論是PC還是Mobile都能自行調整</li>
<li>&nbsp;DashBoard的Chart，善用 DataTable Roles 功能，強化圖表資訊顯示能力&nbsp;</li>
</ol>
<div>
<div>

</div>
</div>
</div>
<div>
<h2>
三、Improve</h2>
</div>
<div>
<ol><span style="background-color: #f7f7f7; color: #333333; font-family: Helvetica, arial, freesans, clean, sans-serif, 'Segoe UI Emoji', 'Segoe UI Symbol'; font-size: 13px; line-height: 33px;"> </span></ol>
<div>
<div>
<ul>
<li>main.py(前端網頁激活)</li>
</ul>
<div>
<div>
</div>
<ol>
<li>Account_Handler使用者登入系統，新增正規表示法，令使用者在當下頁面登入時，也能回到原本的頁面</li>
<li>大幅度簡化main.py的程式碼，去除測試性程式碼與不曾使用的變數</li>
</ol>
</div>
<div>
<ul>
<li>models.py(資料庫的table定義)</li>
</ul>
</div>
</div>
<ol>
<li>配合DashBoard網頁服務，新增Upload_log，觀察上傳流量使用情形</li>
<li>配合DashBoard網頁服務，新增Download_log，觀察下載流量使用情形</li>
</ol>
<div>
<div>
<ul>
<li>methods.py(函數)</li>
</ul>
</div>
<ol>
<li>user_system函數刪除，因為用不到</li>
<li>load_log函數新增，不同的table卻有相同資料庫操作方法，併入其中</li>
<li>Stored_Data_Details類別新增，統合對於Wrapper的資料庫操作方法</li>
</ol>
<div>
<div>
<ul>
<li>customfilters.py(模板擴充)</li>
</ul>
</div>
<ol>
<li>提升可讀性，為了日後維護著想</li>
</ol>
</div>
</div>
</div>
</div>
<div>
<div>
<ul>
<li>網頁重整</li>
</ul>
</div>
<ol>
<li>&nbsp;header的會員訊息，恢復原狀</li>
<li>&nbsp;Clouddrive視覺、操作介面已經大幅度重整</li>
</ol>
<div>
<ul>
<li>js、css配置調整</li>
</ul>
<ol>
<li><span style="background-color: white;">&nbsp;font-awesome-4.1.0更換至4.2.0版，擁有更多合適的icon選擇</span></li>
<span style="background-color: white;">
<li>&nbsp;home.css的動畫延遲功能，獨立成animation-delay.css</li>
</span></ol>
<div>

</div>
</div>
</div>
<div>
<div style="background-color: white; box-sizing: border-box; color: #333333; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans, sans-serif; font-size: 16px; line-height: 25.6000003814697px;">
<h2 style="border-bottom-color: rgb(238, 238, 238); border-bottom-style: solid; border-bottom-width: 1px; box-sizing: border-box; font-size: 1.75em; line-height: 1.225; margin-bottom: 16px; margin-top: 1em; padding-bottom: 0.3em; position: relative;">
<span style="background-color: transparent;">四、Misson</span></h2>
</div>
</div>
<div>
<ol>
<li>&nbsp;Cloud drive顯示檔案需要"切換為清單"以及"切換為格狀"</li>
<li>&nbsp;Cloud drive對於檔案要有判別格式的能力</li>
<li>&nbsp;Cloud drive判別流量是否允許使用者繼續使用服務</li>
<li>&nbsp;Cron的工作排程設定使用無效，並未達成預期，需要改進</li>
</ol>
<div>

</div>
</div>
<div>
</div>
<div>
<div>
<h2>
五、Review</h2>
</div>
<div>
<ol>
<li>DashBoard，該網路服務已完成了！感動～！！</li>
<li>與上次的Push時間間隔真大，中間倒是調整了滿多細節與優化</li>
</ol>
<div>
</div>
</div>
</div>
