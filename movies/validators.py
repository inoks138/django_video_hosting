def validate_video_file(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == '.mp4':
        raise ValidationError('Unsupported file extension.')
