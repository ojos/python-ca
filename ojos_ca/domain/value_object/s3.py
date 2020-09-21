from ojos_ca.domain.value_object.core import IsInstance, Choice
from ojos_ca.domain.value_object.num import Range


class S3Key(IsInstance):
    CLASS_INFO = str

    def pre_set(self, value):
        if isinstance(value, bytes):
            return value.decode()
        else:
            return value

class S3ACL(Choice):
    ALLOW_NONE = True
    CHOICES    = [
        'private',
        'public-read',
        'public-read-write',
        'aws-exec-read',
        'authenticated-read',
        'bucket-owner-read',
        'bucket-owner-full-control',
        'log-delivery-write',
    ]

class S3ObjectBody(IsInstance):
    ALLOW_NONE = True
    CLASS_INFO = (bytes, str)

class S3ObjectContentType(Choice):
    CHOICES = [
        'binary/octet-stream',
        'text/html',
        'text/css',
        'text/xml',
        'image/gif',
        'image/jpeg',
        'application/javascript',
        'application/atom+xml',
        'application/rss+xml',
        'text/mathml',
        'text/plain',
        'text/vnd.sun.j2me.app-descriptor',
        'text/vnd.wap.wml',
        'text/x-component',
        'image/png',
        'image/tiff',
        'image/vnd.wap.wbmp',
        'image/x-icon',
        'image/x-jng',
        'image/x-ms-bmp',
        'image/svg+xml',
        'image/webp',
        'application/font-woff',
        'application/java-archive',
        'application/json',
        'application/mac-binhex40',
        'application/msword',
        'application/pdf',
        'application/postscript',
        'application/rtf',
        'application/vnd.apple.mpegurl',
        'application/vnd.ms-excel',
        'application/vnd.ms-fontobject',
        'application/vnd.ms-powerpoint',
        'application/vnd.wap.wmlc',
        'application/vnd.google-earth.kml+xml',
        'application/vnd.google-earth.kmz',
        'application/x-7z-compressed',
        'application/x-cocoa',
        'application/x-java-archive-diff',
        'application/x-java-jnlp-file',
        'application/x-makeself',
        'application/x-perl',
        'application/x-pilot',
        'application/x-rar-compressed',
        'application/x-redhat-package-manager',
        'application/x-sea',
        'application/x-shockwave-flash',
        'application/x-stuffit',
        'application/x-tcl',
        'application/x-x509-ca-cert',
        'application/x-xpinstall',
        'application/xhtml+xml',
        'application/xspf+xml',
        'application/zip',
        'application/octet-stream',
        'audio/midi',
        'audio/mpeg',
        'audio/ogg',
        'audio/x-m4a',
        'audio/x-realaudio',
        'video/3gpp',
        'video/mp2t',
        'video/mp4',
        'video/mpeg',
        'video/quicktime',
        'video/webm',
        'video/x-flv',
        'video/x-m4v',
        'video/x-mng',
        'video/x-ms-asf',
        'video/x-ms-wmv',
        'video/x-msvideo',
        'application/x-directory',
    ]

class S3ObjectCacheControl(IsInstance):
    ALLOW_NONE = True
    CLASS_INFO = str

class S3ObjectContentEncoding(Choice):
    ALLOW_NONE = True
    CHOICES    = [
        'gzip',
        'compress',
        'deflate',
        'identity',
        'br',
    ]

class S3SummarySize(Range):
    CLASS_INFO = int

