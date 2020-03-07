with open('./A1AVM19970414D064288P1395P360_200UCG6004/A1AVM19970414D064288P1395P360_200UCG6004.02',mode='rb') as fp:
    head = 9360
    
    fp.seek(head + 92,0)
    print('半球: {}'.format(float(fp.read(4).decode('utf-8'))))
    print('UTMゾーン番号: {}'.format(int(fp.read(12).decode('utf-8'))))
    fp.seek(head + 140,0)
    print('シーンセンターの位置（北）: {}'.format(float(fp.read(16).decode('utf-8'))))
    print('シーンセンターの位置（東）: {}'.format(float(fp.read(16).decode('utf-8'))))
    fp.seek(head + 204,0)
    print('地図投影軸と真北のなす角（ラジアン）: {}'.format(float(fp.read(16).decode('utf-8'))))
    fp.seek(head + 540,0)
    print('公称出力ピクセル間隔（メートル）: {}'.format(float(fp.read(16).decode('utf-8'))))
    print('公称出力ライン間隔（メートル）: {}'.format(float(fp.read(16).decode('utf-8'))))
    fp.seek(head + 956,0)
    print('ライン/ピクセルから緯度を求める係数: {}'.format(fp.read(144).decode('utf-8')))
    print('ライン/ピクセルから経度を求める係数: {}'.format(fp.read(144).decode('utf-8')))
    fp.seek(head + 1532,0)
    print('ライン/ピクセルから南北方向のメーター距離を求める係数: {}'.format(fp.read(144).decode('utf-8')))
    print('ライン/ピクセルから東西方向のメーター距離を求める係数: {}'.format(fp.read(144).decode('utf-8')))
    
    