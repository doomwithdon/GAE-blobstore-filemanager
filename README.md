版本:0.1.0.0

=============

新增:
1.表格化

debug:
1.django的filter函數要與|相鄰
  例如:{{ wrapper.blob.size|countByte }}  is O
       {{ wrapper.blob.size| countByte }} is X
