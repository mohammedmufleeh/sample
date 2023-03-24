from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# from MetaTrader5 import SymbolInfoTick, SymbolInfo, ORDER_TYPE_BUY, ORDER_TYPE_SELL, TRADE_ACTION_DEAL, ORDER_TIME_GTC, ORDER_FILLING_IOC, order_send

@csrf_exempt
def execute_trade(request):
    if request.method == 'POST':
        # Get request data
        action = request.POST.get('action')
        symbol = request.POST.get('symbol')
        lot = float(request.POST.get('lot'))
        sl_points = float(request.POST.get('sl_points'))
        tp_points = float(request.POST.get('tp_points'))
        deviation = int(request.POST.get('deviation'))

        # Validate request data
        if action not in ['buy', 'sell']:
            return JsonResponse({'error': 'Invalid action'})
        if not SymbolInfo(symbol).name:
            return JsonResponse({'error': 'Invalid symbol'})
        if lot <= 0:
            return JsonResponse({'error': 'Invalid lot size'})
        if sl_points < 0 or tp_points < 0 or deviation < 0:
            return JsonResponse({'error': 'Invalid parameter values'})

        # Execute trade
        if action == 'buy':
            trade_type = ORDER_TYPE_BUY
            price = SymbolInfoTick(symbol).ask
        else:
            trade_type = ORDER_TYPE_SELL
            price = SymbolInfoTick(symbol).bid

        point = SymbolInfo(symbol).point

        buy_request = {
            "action": TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": trade_type,
            "price": price,
            "sl": price - sl_points * point,
            "tp": price + tp_points * point,
            "deviation": deviation,
            "magic": ea_magic_number,
            "comment": "sent by python",
            "type_time": ORDER_TIME_GTC, # good till cancelled
            "type_filling": ORDER_FILLING_IOC,
        }

        result = order_send(buy_request)

        if result.retcode == 0:
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': result.comment})
    else:
        return JsonResponse({'error': 'Invalid request method'})
