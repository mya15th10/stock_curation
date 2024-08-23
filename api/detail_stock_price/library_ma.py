from api.extension import ma
class detailSchema(ma.Schema):
    class Meta:
        fields = ('id', 'stock_id', 'session_id', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')