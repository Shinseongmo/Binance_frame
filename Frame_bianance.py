import ccxt
import time 

A=0

#---코인 매수 매도 비율 변수
symbol0 =input('종목 입력 (EX:BTC/USDT): ') # symbol0=코인
leverage1 =int(input('레버리지 입력: '))
input_rate= int(input('진입비율 입력: '))
#42줄 amount0 변경

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #기본 정보 셋팅
print('API를 입력해주세요')
print('')
binance = ccxt.binance(config={
    'apiKey': input('api_key : '),
    'secret': input('secret_key : '),
    'enableRateLimit': True, 
    'options': {
        'defaultType': 'future'
    }
})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#시장 정보 가져오기
markets = binance.load_markets()
symbol = symbol0
market = binance.market(symbol)
#레버리지 정보
binance.fapiPrivate_post_leverage({
    'symbol': market['id'],
    'leverage': leverage1
})
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#코인 가격 불러오기
ticker = binance.fetch_ticker(symbol0)
coin_last = float(ticker['last'])
#지갑 잔고 불러오기
balance_wallet = binance.fetch_balance()
#잔고 업데이트하기
last_wallet= float(balance_wallet['total']['USDT'])
print('')
print('현재 선물 잔고를 알려드립니다.:', end=' ')
print(last_wallet)
print('')
# 주문량 
amount0=float(((last_wallet)*leverage1*float(input_rate))/(100*coin_last))


while True:
    ticker = binance.fetch_ticker(symbol0)
    coin_last = float(ticker['last'])
    print('1:롱 매수, 2:롱 매도, 3:숏 매수, 4:숏 매도', end='  ')
    print('(**롱은 상승 숏은 하락에 따라 수익을 얻습니다.**)')
    A=int(input('매수주문을 체결할게요 위 번호 중 하나를 눌러주세요: '))
    print('')
    # 롱 매수과 롱 매도
    if A == 2 or A == 4:
        print('매수부터 진행하세요.')
        print('')
        continue
    if A == 1:
        print('롱 체결')
        print('')
        order=binance.create_market_buy_order(symbol=symbol0, amount='{}'.format(amount0), params = {'positionSide':'LONG'})       
        A=int(input('매도주문을 체결할게요. 2을 눌러주세요.: '))
        print('')
        if A == 2:
            print('롱 매도')
            print('')
            order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'LONG'})    
            A=int(input(('계속 진행한다면 5를 눌러주세요.: ')))
            print('')
            if A == 5:
                print('처음으로 돌아갑니다.')
                print('')
                continue   
            else:
                print('매매 종료') 
                print('')
                break
    # 숏 매수와 숏 매도   
    if A == 3:        
        print('숏 체결') 
        print('')      
        order = binance.create_market_sell_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
        A=int(input('매도주문을 체결할게요. 4을 눌러주세요. : '))
        print('')
        if A == 4:
            print('숏 매도')
            print('')
            order = binance.create_market_buy_order(symbol=symbol0,amount='{}'.format(amount0),params = {'positionSide': 'SHORT'})
            A=int(input(('계속 진행한다면 6를 눌러주세요.: ')))
            print('')
            if A == 6:
                print('처음으로 돌아갑니다.')
                print('')
                continue   
            else:
                print('매매 종료') 
                print('')
            break  