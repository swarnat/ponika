from ponika import PonikaClient


connection = PonikaClient(
    host='10.72.1.97',
    username='admin',
    password='svyJ4bj1L=36R8%$',
    # Optional, default is True, but often there no valid certificate
    verify_tls=False,
)
