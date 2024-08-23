from api.extension import ma

class stockSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'code', 'country', 'stock_space', 'join_date', 'leave_date', 'init_price', 'updated_at', 'created_at', 'created_by', 'category', 'is_index')