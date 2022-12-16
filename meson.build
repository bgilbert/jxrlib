project(
  'jxrlib',
  'c',
  default_options : [
    'buildtype=debugoptimized',
    'warning_level=0',
  ],
  license : 'BSD-2-Clause',
  meson_version : '>=0.50',
  version : '1.1',
)
soversion = '0.0.0'

# dependencies
cc = meson.get_compiler('c')
m_dep = cc.find_library('m', required : false)

# compiler options
add_project_arguments(
  '-D__ANSI__',
  '-DDISABLE_PERF_MEASUREMENT',
  language: 'c',
)
if host_machine.endian() == 'big'
  add_project_arguments(
    '-D_BIG__ENDIAN_',
    language : 'c',
  )
endif

install_headers(
  'common/include/guiddef.h',
  'common/include/wmsal.h',
  'common/include/wmspecstring.h',
  'common/include/wmspecstrings_adt.h',
  'common/include/wmspecstrings_strict.h',
  'common/include/wmspecstrings_undef.h',
  'image/sys/windowsmediaphoto.h',
  'jxrgluelib/JXRGlue.h',
  'jxrgluelib/JXRMeta.h',
  'jxrtestlib/JXRTest.h',
  subdir : 'jxrlib',
)

jpegxr_include = [
  'common/include',
  'image/sys',
]
jpegxr = library(
  'jpegxr',
  'image/decode/decode.c',
  'image/decode/JXRTranscode.c',
  'image/decode/postprocess.c',
  'image/decode/segdec.c',
  'image/decode/strdec.c',
  'image/decode/strInvTransform.c',
  'image/decode/strPredQuantDec.c',
  'image/encode/encode.c',
  'image/encode/segenc.c',
  'image/encode/strenc.c',
  'image/encode/strFwdTransform.c',
  'image/encode/strPredQuantEnc.c',
  'image/sys/adapthuff.c',
  'image/sys/image.c',
  'image/sys/perfTimerANSI.c',
  'image/sys/strcodec.c',
  'image/sys/strPredQuant.c',
  'image/sys/strTransform.c',
  dependencies : [m_dep],
  include_directories : jpegxr_include,
  install : true,
  version : soversion,
)

jxrglue_include = [
  jpegxr_include,
  'jxrgluelib',
  'jxrtestlib',
]
jxrglue = library(
  'jxrglue',
  'jxrgluelib/JXRGlue.c',
  'jxrgluelib/JXRGlueJxr.c',
  'jxrgluelib/JXRGluePFC.c',
  'jxrgluelib/JXRMeta.c',
  'jxrtestlib/JXRTestBmp.c',
  'jxrtestlib/JXRTest.c',
  'jxrtestlib/JXRTestHdr.c',
  'jxrtestlib/JXRTestPnm.c',
  'jxrtestlib/JXRTestTif.c',
  'jxrtestlib/JXRTestYUV.c',
  dependencies : [m_dep],
  include_directories : jxrglue_include,
  install : true,
  link_with : [jpegxr],
  version : soversion,
)

import('pkgconfig').generate(
  jxrglue,
  description : 'A library for reading JPEG XR images',
  name : 'libjxr',
  url : 'https://github.com/bgilbert/jxrlib',
)

enc = executable(
  'JxrEncApp',
  'jxrencoderdecoder/JxrEncApp.c',
  include_directories : jxrglue_include,
  install : true,
  link_with : [jxrglue],
)

enc420 = executable(
  'JxrEnc420',
  'jxrencoderdecoder/JxrEnc420.c',
  include_directories : jxrglue_include,
  link_with : [jxrglue],
)

dec = executable(
  'JxrDecApp',
  'jxrencoderdecoder/JxrDecApp.c',
  include_directories : jxrglue_include,
  install : true,
  link_with : [jxrglue],
)

dec420 = executable(
  'JxrDec420',
  'jxrencoderdecoder/JxrDec420.c',
  include_directories : jxrglue_include,
  link_with : [jxrglue],
)

jxrlib_dep = declare_dependency(
  link_with : [jxrglue],
)

test(
  'decode',
  files('test/decode.py'),
  args : [dec],
  # avoid timeout during download
  timeout : 1800,
)
