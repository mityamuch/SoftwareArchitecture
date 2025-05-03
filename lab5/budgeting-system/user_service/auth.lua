token = nil
auth_done = false

request = function()
    if not auth_done then
        auth_done = true
        return wrk.format(
            "POST",
            "/token",
            {["Content-Type"] = "application/x-www-form-urlencoded"},
            "username=admin&password=secret"
        )
    end
    
    if not token then
        return wrk.format("GET", "/users/1")
    end
    
    local headers = {
        ["Authorization"] = token,
        ["Content-Type"] = "application/json"
    }
    
    return wrk.format("GET", "/users/1", headers)
end

response = function(status, headers, body)
    if not token and status == 200 then
        token = string.match(body, '"access_token":"([^"]+)"')
        if token then
            token = "Bearer " .. token
            print("Successfully obtained token:", token)
        end
    end
    
    if status == 401 then
        print("Received 401 Unauthorized - token may have expired")
    end
end