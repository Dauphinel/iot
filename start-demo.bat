@echo off
echo ========================================
echo    🚀 IoT Pipeline Demo - Starting
echo ========================================
echo.
echo Starting all services...
docker-compose up -d
echo.
echo Waiting for services to start...
timeout /t 10 /nobreak > nul
echo.
echo ========================================
echo    ✅ Services Started Successfully!
echo ========================================
echo.
echo 📊 Grafana Dashboard: http://localhost:3000
echo    Username: admin
echo    Password: admin
echo.
echo 📡 MQTT Broker: localhost:1883
echo 📊 InfluxDB: http://localhost:8086
echo 🚀 Kafka: localhost:9092
echo.
echo 🔍 Check logs with: docker-compose logs -f
echo 🛑 Stop with: docker-compose down
echo.
pause 