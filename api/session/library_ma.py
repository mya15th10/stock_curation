from api.extension import ma

class sessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'quarter', 'day_of_week', 'day_of_month', 'month', 'year', 'volume', 'updated_at', 'created_at', 'updated_by', 'created_by')