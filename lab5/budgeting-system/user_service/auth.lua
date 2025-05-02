token = nil

request = function()
    if not token then
        local credentials = '{"username":"admin", "password":"secret"}'
        local res = wrk.format("POST", "/token", {["Content-Type"]="application/x-www-form-urlencoded"}, "username=testuser&password=testpass")
        response = wrk.execute(res)
        if response.status == 200 then
            token = "Bearer " .. string.match(response.body, '"access_token":"([^"]+)"')
        end
    end
    
    local headers = {
        ["Content-Type"] = "application/json",
        ["Authorization"] = token
    }
    return wrk.format("GET", "/users/1", headers)
end