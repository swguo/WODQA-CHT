import filter1 as f1
import filter2 as f2
import filter3 as f3
import QGmodel as qg
import QAmodel as qa
import eval as evl
import argparse

def main(args):
  if args.text == 'all':
    # 挑選合適的 Entity
    f1.run()
    # 透過 Entity 生成 QA pair
    qg.run()
    # QA 訊息量檢測
    f2.run()
    # filter 3 google seach
    f3.run()
    # 執行 QA 預測
    qa.run('pred_f3_cn','odqa_f3_cn')
    # 評估分數
    evl.run('pred_f3_cn','odqa_f3_cn')

  elif args.text == 'f1':
    # 挑選合適的 Entity
    f1.run()
    # 透過 Entity 生成 QA pair
    qg.run()
    # 執行 QA 預測
    qa.run('pred_f2_cn','odqa_f2_cn')
    # 評估分數
    evl.run('pred_f2_cn','odqa_f2_cn')
  elif args.text == 'f2':
    # 挑選合適的 Entity
    f1.run()
    # 透過 Entity 生成 QA pair
    qg.run()
    # 執行 Filter 2
    f2.run()
    # 執行 QA 預測
    qa.run('pred_f2_cn','odqa_f2_cn')
    # 評估分數
    evl.run('pred_f2_cn','odqa_f2_cn')
  else:
    print('error')
  

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog='main.py', description='Tutorial') 
    parser.add_argument('--text', '-t', default='all', type=str, required=False,  help='Text for program')
    args = parser.parse_args()
    main(args)
