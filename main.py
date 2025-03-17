import requests
import json

API_KEY = "1bc977fb87dceb0277dbc4e0086b8023"  # 替换成自己的APIKEY
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name):
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': 'metric'  # 使用摄氏温度
    }

    try:
        response = requests.get(BASE_URL, params=params)    # Get申请
        response.raise_for_status() # HTTP状态码
        data = response.json()

        if data["cod"] != 200:  # 不是200，抛出异常
            return None

        return {
            'city': data['name'],
            'temp': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'wind_speed': data['wind']['speed']
        }

    #异常问题
    except requests.exceptions.RequestException as e:
        print(f"网络错误: {str(e)}")
        return None
    except (KeyError, json.JSONDecodeError):
        print("无效的API响应")
        return None


def main():
    print("===== 天气查询应用 =====")
    print("输入多个城市时用逗号分隔（例如：北京,上海）")
    print("输入 'exit' 退出程序\n")

    while True:
        cities = input("请输入城市名称: ").strip()

        if cities.lower() == 'exit':    # 自定义退出信号
            print("感谢使用！")
            break

        if not cities:
            print("请输入有效的城市名称")
            continue

        city_list = [city.strip() for city in cities.split(',')]

        for city in city_list:
            weather_data = get_weather(city)

            if weather_data:
                print("\n" + "=" * 40)
                print(f"城市: {weather_data['city']}")
                print(f"温度: {weather_data['temp']}°C")
                print(f"湿度: {weather_data['humidity']}%")
                print(f"天气状况: {weather_data['description'].capitalize()}")
                print(f"风速: {weather_data['wind_speed']} m/s")
                print("=" * 40 + "\n")
            else:
                print(f"\n无法获取 {city} 的天气信息，请检查城市名称是否正确\n")


if __name__ == "__main__":
    main()
