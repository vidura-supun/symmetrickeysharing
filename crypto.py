#!/usr/bin/python

from cryptography.fernet import Fernet


key = b"ueTVbnjTPFYhhuYsLSC2nl9GF9CMJ3tkkkaMmyMpNws="
cipher_suite = Fernet(key)
#cipher_text = cipher_suite.encrypt(b"A really secret message. Not for prying eyes.")
plain_text = cipher_suite.decrypt(b"gAAAAABcW-t3SP5NWJpJCMqHR1fkURoffr_6HAvqV_PAmag09Drtj9syhwuWvxiMOiUlEBfbWlUf1Zn1dp3FzUf3tn6E2vazrTvUXfUD78u_JqUFJ-RWysvk9Zv8mKHjLf-GGVC-w1cQ").decode("utf-8")

print(plain_text)
