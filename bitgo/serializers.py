from io import BytesIO
import qrcode
from rest_framework import serializers

from bitgo.models import Address



class AddressSerializer(serializers.ModelSerializer):
    qr_code = serializers.SerializerMethodField()

    class Meta:
        model = Address
        fields = ['id', 'address', 'profile', 'wallet', 'bitgo_wallet', '_is_active', 'qr_code']

    def get_qr_code(self, obj):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(obj.address)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        qr_img.save(buffer, format='PNG')
        qr_bytes = buffer.getvalue()
        return qr_bytes