# Тест без кеша (1 поток)
wrk -t1 -c1 -d10s -s auth.lua http://localhost:8003

# Тест без кеша (5 потоков)
wrk -t5 -c5 -d10s -s auth.lua http://localhost:8003

# Тест без кеша (10 потоков)
wrk -t10 -c10 -d10s -s auth.lua http://localhost:8003

# Тест с кешем (1 поток)
wrk -t1 -c1 -d10s -s auth.lua http://localhost:8003

# Тест с кешем (5 потоков)
wrk -t5 -c5 -d10s -s auth.lua http://localhost:8003

# Тест с кешем (10 потоков)
wrk -t10 -c10 -d10s -s auth.lua http://localhost:8003