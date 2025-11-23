import os
from datetime import datetime
import base64

from OpenSSL import crypto
from db.models import Device
from config.config import ca_config
from config.logs_config import logger

from cast_types.g_types import DbSessionType


CA_KEY_FILE = ca_config.CA_KEY_FILE
CA_CERT_FILE = ca_config.CA_CERT_FILE
CRL_FILE = ca_config.CRL_FILE


def sign_csr(csr_pem, subject_cn):
    """Sign provided certificate"""
    logger.info("Decoding CSR")
    csr_pem = base64.b64decode(csr_pem)
    logger.info("Loading CSR")
    csr = crypto.load_certificate_request(crypto.FILETYPE_PEM, csr_pem)
    logger.info("Loading CA certificate")
    ca_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, open(CA_CERT_FILE, "rb").read()
    )
    logger.info("Loading CA private key")
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(CA_KEY_FILE, "rb").read())
    cert = crypto.X509()
    cert.set_serial_number(int.from_bytes(os.urandom(8), "big"))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(90 * 24 * 60 * 60)  # valid 90 days
    cert.set_issuer(ca_cert.get_subject())
    cert.set_subject(csr.get_subject())
    cert.set_pubkey(csr.get_pubkey())
    cert.sign(ca_key, "sha256")

    return crypto.dump_certificate(crypto.FILETYPE_PEM, cert), cert


def generate_crl(db: DbSessionType):
    """Write Certificates Revocation List to file"""
    ## TODO. Fix it
    ca_cert = crypto.load_certificate(
        crypto.FILETYPE_PEM, open(CA_CERT_FILE, "rb").read()
    )
    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM, open(CA_KEY_FILE, "rb").read())
    revoked_devices = db.query(Device).filter(Device.status == "revoked").all()

    crl = crypto.load
    for device in revoked_devices:
        if device.cert_serial:
            revoked_cert = crypto.Revoked()
            revoked_cert.set_serial(device.cert_serial.encode())
            revoked_cert.set_reason(b"unspecified")
            revoked_cert.set_rev_date(datetime.now().strftime("%Y%m%d%H%M%SZ").encode())
            crl.add_revoked(revoked_cert)

    crl_pem = crl.export(ca_cert, ca_key, crypto.FILETYPE_PEM)
    with open(CRL_FILE, "wb") as f:
        f.write(crl_pem)
