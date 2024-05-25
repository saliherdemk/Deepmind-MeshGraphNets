<style>
    /* .heatMap { */
    /*     width: 100%; */
    /*     text-align: center; */
    /* } */
    .heatMap th {
        word-wrap: break-word;
        text-align: center;
    }
 .heatMap tr:nth-child(even) {
    background-color: transparent !important;
  }
</style>

<div class="heatMap">

| Sütun | Şekil| Anlam| 
| -- | ---- | -- | 
| cells | (1, 3362, 3) &nbsp;&nbsp;&nbsp;&nbsp;| Mesh noktaları arasındaki bağlantıları temsil eder. |
| mesh_pos | (1, 1764, 2) | Mesh noktalarının iki boyutlu koordinatlarını temsil eder. |
| node_type | (250, 1764, 1) | Mesh noktalarının türü hakkında bilgi saklar.| 
| world_pos | (250, 1764, 3) | Mesh noktalarının üç boyutlu düzlemdeki gerçek koordinatlarını temsil eder.|
| wind_training | (250, 3) | Ön işlem gerçekleştirilmiş rüzgar vektörünü içerir.|
| wind | (250, 4) | Saf rüzgar bilgisini içerir. Yalnızca simülasyon için gereklidir.|

</div>

