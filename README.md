#SoXSearch#

SoXSearch repository

##API Usage##

You can search registered nodes in [sox.ht.sfc.keio.ac.jp][1] by

 - node name
 - node type
 - node location (latitude & longitude required)

### Endpoint URL

- http://133.27.174.34/api/search

 Use **HTTP GET** to call this API (**POST** currently not supported...)

###Query Example: 

#### Search by node name 

> http://133.27.174.34/api/search?**name=hogehoge**

#### Search by node type

> http://133.27.174.34/api/search?**type=mogemoge**

#### Search by node location

> http://133.27.174.34/api/search?**lat=35.00&lon=135.00**
 
> additionally, nodes can be searched within a range(unit: meter) like below

> http://133.27.174.34/api/search?lat=35.00&lon=135.00&**radius=100**


###jQuery Code Exmaple###

    # javascript
    function searchNode() {
        $.ajax({
            url: "http://133.27.174.34/api/search",
            type: "GET",
            dataType: "json",
            data: {
                name: "Tokyo",
                type: "outdoor weather",
                lat: 35.658581,
                lng: 139.745433,
                radius: 100
            }
            success: function(json) {
                console.log(json);
            }
        });
    }

[1]: http://sox.ht.sfc.keio.ac.jp
