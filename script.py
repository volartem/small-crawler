import requests
from scrapy.http import TextResponse
import sys


def get_url_bnb(lat=39.684948, lon=-104.892813):
    """ This function will automatically generate search 
        urls for any given lat long with optimal box size.
        The return search url should result in less than 17
        pages (max number of pages allowed on Airbnb)

        lat: Latitude of the select location
        lon: Longitude of the select location
        :return: The url and how many pages for the box
    """

    # Start with lat +- 0.1  and long +- 0.1
    i = 0.1
    url = 'https://www.airbnb.com/s?ne_lat=' + str(lat + i) + '&ne_lng=' + str(lon + i) + \
          '&sw_lat=' + str(lat - i) + '&sw_lng=' + str(lon - i) + \
          '&room_types%5B%5D=Entire%20home%2Fapt&room_types%5B%5D=Private%20room' + '&search_by_map=true'
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.21 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8'
    }
    r = session.get(url, headers=headers)
    response = TextResponse(r.url, body=r.text, encoding='utf-8')
    # If more than 17 pages, than reduce the lat long range
    try:
        # TODO  Need to change this since Airbnb changes it's design, can't get the last page number now
        temp = response.xpath('//ul[@class="buttonList_11hau3k"]/li[last()-1]')[0]
        last_page_number = int(temp.xpath(".//text()").extract()[0])
        print "last page is ", last_page_number
    except:

        last_page_number = 17
        pass
    if last_page_number < 17:
        print 'rare situation, only ', last_page_number, 'pages'
        return url, last_page_number
    i = i / 1.2
    while last_page_number == 17:
        url = 'https://www.airbnb.com/s?ne_lat=' + str(lat + i) + '&ne_lng=' + str(lon + i) + \
              '&sw_lat=' + str(lat - i) + '&sw_lng=' + str(lon - i) + '&search_by_map=true'
        r = session.get(url, headers=headers)
        response = TextResponse(r.url, body=r.text, encoding='utf-8')
        try:
            temp = response.xpath('//ul[@class="buttonList_11hau3k"]/li[last()-1]')[0]
            last_page_number = int(temp.xpath(".//text()").extract()[0])
            print "last page is %s lat + i=%s long + i=%s lat - i=%s long - i=%s" % \
                  (last_page_number, lat + i, lon + i, lat - i, lon - i)
        except:
            if last_page_number == 17:
                continue
            else:
                print 'Something bad happend', last_page_number, url
                return url, last_page_number
        if last_page_number <= 5:
            print 'rare situation, only ', last_page_number, 'pages'
            break
        i = i / 1.15
    return url, last_page_number


def main():
    # Test request regions
    lons = [-104.89277, -121.827144, -104.870008, -122.213547, -118.274061, -118.389202, -122.418148, \
            -80.868115, -81.288805, -121.892831, -81.473779, -84.511157, -87.625901, -87.63382, -96.795619, -122.408903, \
            -118.349027, -104.941913, -81.394798, -84.385389, -90.092082, -118.536463, -112.055596, -111.878806,
            -122.414861]
    lats = [39.684878, 37.382807, 39.693106, 37.4737, 34.062426, 33.988818, 37.787212, 35.125602, 28.520925, \
            37.349202, 28.408372, 33.73447, 41.885574, 41.913773, 32.777525, 37.773481, 34.062111, 39.71, \
            28.5327, 33.774045, 29.958904, 34.191076, 33.524718, 40.682182, 37.787486]

    # Second test request region
    # lons = [-76.291534]
    # lats = [36.852724]
    num_of_location = 0
    urls = []
    if len(sys.argv) <= 2:
        print 'Not enough input, use last request data. lat = ', lats, ' long = ', lons
        sys.argv.append('work_file_session')
    elif len(sys.argv) % 2 != 0:
        print 'In valid input, need to be lat long pairs, example ' \
              'python generate_url location_name lat1 long1 lat2 long2 ...'
    else:
        lats = []
        lons = []
        num_of_location = len(sys.argv) / 2 - 1
        for i in range(num_of_location):
            lats.append(float(sys.argv[i * 2 + 2]))
            lons.append(float(sys.argv[i * 2 + 3]))
    print 'There are ', num_of_location, ' lat long pairs, stop if the number is not correct'
    for i in range(len(lats)):
        print i + 1, 'th listing lat = ', lats[i], ' long = ', lons[i]
        url, n = get_url_bnb(lats[i], lons[i])
        urls.append(url)
        print 'The ', i + 1, 'th listing', lats[i], lons[i], ' number of listings will get ', n
        print 'url = ', url

    with open(sys.argv[1] + '.txt', 'w') as f:
        for i in urls:
            f.write(i + '\n')

if __name__ == '__main__':
    main()
