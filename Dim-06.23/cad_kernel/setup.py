#
# Copyright (c) 2002, 2003, 2004, 2005, 2006, 2007 P.Reunamo
#

#
# Install cad_kernel using the distutils method
#

from distutils.core import setup

setup(name="cad_kernel",
      version="0.02",
      description="CAD kernel",
      author="Petteri Reunamo",
      author_email="petteri.reunamo@samk.fi",
      url="http://www.tp.spt.fi/~lapere",
      license="GPL",
      packages=['cad_kernel'])
