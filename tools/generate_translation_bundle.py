# -*- coding: utf-8 -*

'''Bootstrapping for GRIT.
'''

import os
import sys
#import argparse
import optparse
import subprocess
import xml.dom.minidom as minidom

def PrintUsage():
  print( """
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Usage: generate_translation_bundle [options]

options:

  --old_grd 

  --new_grd
  
  --old_xtb
  
  -o,--output  
  
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
""")

def _ParseOptions(): 
  #parser = argparse.ArgumentParser(description='Change file names.')
  parser = optparse.OptionParser()
  # metavar only changes the displayed name
  # first argument (w/o '-') used as positional argument
  # argument with '-' will be used as optional argument
  # nargs '?' will treat input as string, 
  # while '+' for list
  parser.add_option('--old_grd', 
                     help='original grd file')
  parser.add_option('--new_grd', 
                     help='modified grd file')
  parser.add_option('--old_xtb', 
                     help='original xtb file')                   
  parser.add_option('-o', '--output', 
                     help='output directory')                   
  # parse cmdline arguments to an object
  # then pass to main
  args, _  = parser.parse_args()
  if not args.old_grd:
    parser.error('You must provide a origin grd file.')
  if not args.new_grd:
    parser.error('You must provide a modified grd file.')
  if not args.old_xtb:
    parser.error('You must provide a origin xtb file.')    
  return args


#--------------------------------
# 读取 xml 文件，返回 dom 对象
def getXmlObj(filePath, mode):
  return minidom.parse(filePath)
  
def getElementByAttributeFromList(elements, attr, value):
  for idx,ele in enumerate(elements):
    if ele.getAttribute(attr)==value:
      return (idx,ele)
  return (-1,None)
  
def getElementByAttribute(root, tag, attr, value):
  elements = root.getElementsByTagName(tag)
  for idx,ele in enumerate(elements):
    if ele.getAttribute(attr)==value:
      return (idx,ele)
  return (-1,None)
  
def generateTranslationBundle(oldGrdPath, newGrdPath, oldXtbPath):
  # 取得根
  oldGrdDoc = getXmlObj(oldGrdPath, 'r')
  newGrdDoc = getXmlObj(newGrdPath, 'r')
  oldXtbDoc = getXmlObj(oldXtbPath, 'r')
  # 取得结点数组
  oldGrdNodes = oldGrdDoc.getElementsByTagName("translation")
  newGrdNodes = newGrdDoc.getElementsByTagName("translation")
  oldXtbNodes = oldXtbDoc.getElementsByTagName("translation")
  
  outSame = ''
  outModified = ''
  outNew = ''
  
  for idx,newIdEle in enumerate(newGrdNodes):
    newId = newIdEle.getAttribute('id')
    
    # 尝试通过 id 直接从译文中找对应的翻译
    foundId,foundEle = getElementByAttributeFromList(oldXtbNodes, 'id', newId)
    
    # 找到，说明grd未改，id未变, 直接使用旧翻译
    if foundEle is not None:
      outSame += "%s\n" % foundEle.toxml()
    
    else:
      # 通过 id 没找到，但 current index 小于 old grd 的总结点数，
      # 先尝试通过与旧grd对应关系获取旧翻译
      if idx <oldGrdNodes.length:
        # !!!这里简单的通过index来匹配旧的翻译结点，所以要保证新旧2个版本GRD文档的对应顺序 
        foundId,foundEle = getElementByAttributeFromList(oldXtbNodes, 'id', oldGrdNodes[idx].getAttribute('id') )   
    
      # 获取到旧翻译，仍旧输出旧翻译作为参考，并标记“需要更新”
      if foundEle is not None:
        foundEle.setAttribute('id', newId)
        foundEle.setAttribute('TODO', 'NEED-UPDATE')
        outModified += "%s\n" % foundEle.toxml()
      # 原先该grd的结点，就没对应的翻译
      else:
        newIdEle.setAttribute('TODO', 'NEED-TRANSLATE')
        outNew += "%s\n" % newIdEle.toxml()
 
  return outSame+outModified+outNew
         
def main(args):
  # 检查python版本
  if sys.version_info < (2, 6):
    print( "GRIT requires Python 2.6 or later." )
    return
    
  # 打印帮助  
  elif not args or (len(args) == 1 and args[0] == 'help'):
    PrintUsage()
    return 0
    
  options = _ParseOptions()  
  
  # 输入的 old grd 路径
  oldGrdPath =  options.old_grd 
  # 输入的 new grd 路径
  newGrdPath = options.new_grd 
  # 输出的目录
  outputDir = os.path.dirname(options.output)
  # 输出的文件名，不包含扩展名
  outputFileName = os.path.splitext(os.path.basename(options.output))[0]
  # old grd 生成的中间文件
  outputOldGrdPath = os.path.join(outputDir,outputFileName+'.old.tmp')
  # new grd 生成的中间文件
  outputNewGrdPath = os.path.join(outputDir,outputFileName+'.new.tmp')
  
  # 处理 old grd 文件
  # 通过 grit.py 调用子工具，常用的有：xmb，build。详情见 grit_runner.py
  # xmb 的参数详情见 tool/xmb.py
  # Other options:
  # -D NAME[=VAL]     Specify a C-preprocessor-like define NAME with optional
  #                  value VAL (defaults to 1) which will be used to control
  #                  conditional inclusion of resources.
  # -E NAME=VALUE     Set environment variable NAME to VALUE (within grit).
  subprocess.call([
      'python', 
      "grit/grit.py",
      '-i', oldGrdPath, 
      'xmb', 
      '-D', '_chromium', 
      '-D', 'toolkit_views', 
      '-D', 'use_aura', 
      '-D', 'use_ash', 
      '-D', 'enable_extensions', 
      '-D', 'enable_plugins', 
      '-D', 'enable_printing', 
      '-D', 'enable_print_preview',
      '-D', 'enable_themes', 
      '-D', 'enable_app_list', 
      '-D', 'enable_settings_app', 
      '-D', 'enable_google_now', 
      '-D', 'use_concatenated_impulse_responses', 
      '-D', 'enable_webrtc', 
      '-D', 'enable_task_manager', 
      '-D', 'enable_notifications', 
      '-D', 'enable_wifi_bootstrapping', 
      '-D', 'enable_topchrome_md', 
      '-D', 'enable_service_discovery',
      outputOldGrdPath,
      ], 
    shell=True)
      
  # 处理 new grd 文件
  subprocess.call([
      'python', 
      "grit/grit.py",
      '-i', newGrdPath,
      'xmb',
      '-D', '_chromium', 
      '-D', 'toolkit_views', 
      '-D', 'use_aura', 
      '-D', 'use_ash', 
      '-D', 'enable_extensions', 
      '-D', 'enable_plugins', 
      '-D', 'enable_printing', 
      '-D', 'enable_print_preview',
      '-D', 'enable_themes', 
      '-D', 'enable_app_list', 
      '-D', 'enable_settings_app', 
      '-D', 'enable_google_now', 
      '-D', 'use_concatenated_impulse_responses',  
      '-D', 'enable_webrtc', 
      '-D', 'enable_task_manager', 
      '-D', 'enable_notifications', 
      '-D', 'enable_wifi_bootstrapping', 
      '-D', 'enable_topchrome_md', 
      '-D', 'enable_service_discovery',
      outputNewGrdPath,
      ], 
    shell=True)
    
  # 生成 new xtb 文件
  outputString = generateTranslationBundle(outputOldGrdPath, outputNewGrdPath, options.old_xtb);
  
  # 保存到结果文件
  out_file = open(options.output, mode='w', encoding='utf-8')
  out_file.write( '<?xml version="1.0" ?>\n<!DOCTYPE translationbundle>\n<translationbundle lang="zh-CN">\n' )
  out_file.write(outputString)  
  out_file.write( '</translationbundle>' )  
  
 	# 删除中间文件 
  os.remove(outputOldGrdPath)
  os.remove(outputNewGrdPath)

  
# Omitted when being used as module
if '__main__' == __name__:   
  sys.exit(main(sys.argv[1:]))
