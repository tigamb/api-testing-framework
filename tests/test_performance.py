
import allure
import pytest
import time
import statistics


# קבועי זמן בשניות
MAX_RESPONSE_TIME = 2.0
ACCEPTABLE_RESPONSE_TIME = 1.0
FAST_RESPONSE_TIME = 0.5


@allure.feature("Performance")
class TestResponseTimes:

    @allure.title("GET כל הפוסטים - זמן תגובה תקין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_posts_response_time(self, api_client):
        with allure.step("שולח GET ל־/posts ומודד זמן"):
            response = api_client.get("/posts")
            elapsed = response.elapsed.total_seconds()

        with allure.step(f"מוודא שזמן התגובה קטן מ־{MAX_RESPONSE_TIME} שניות"):
            allure.attach(
                f"זמן תגובה: {elapsed:.3f}s",
                name="Response Time",
                attachment_type=allure.attachment_type.TEXT
            )
            assert elapsed < MAX_RESPONSE_TIME, \
                f"זמן תגובה {elapsed:.3f}s עולה על המקסימום {MAX_RESPONSE_TIME}s"

    @allure.title("GET פוסט בודד - זמן תגובה מהיר")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_single_post_response_time(self, api_client):
        with allure.step("שולח GET ל־/posts/1 ומודד זמן"):
            response = api_client.get("/posts/1")
            elapsed = response.elapsed.total_seconds()

        with allure.step(f"מוודא שזמן התגובה קטן מ־{ACCEPTABLE_RESPONSE_TIME} שניות"):
            allure.attach(
                f"זמן תגובה: {elapsed:.3f}s",
                name="Response Time",
                attachment_type=allure.attachment_type.TEXT
            )
            assert elapsed < ACCEPTABLE_RESPONSE_TIME, \
                f"זמן תגובה {elapsed:.3f}s עולה על המקסימום {ACCEPTABLE_RESPONSE_TIME}s"

    @allure.title("POST יצירת פוסט - זמן תגובה תקין")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_post_response_time(self, api_client):
        with allure.step("שולח POST ל־/posts ומודד זמן"):
            new_post = {
                "title": "בדיקת ביצועים",
                "body": "תוכן לבדיקה",
                "userId": 1
            }
            response = api_client.post("/posts", new_post)
            elapsed = response.elapsed.total_seconds()

        with allure.step(f"מוודא שזמן התגובה קטן מ־{MAX_RESPONSE_TIME} שניות"):
            allure.attach(
                f"זמן תגובה: {elapsed:.3f}s",
                name="Response Time",
                attachment_type=allure.attachment_type.TEXT
            )
            assert elapsed < MAX_RESPONSE_TIME, \
                f"זמן תגובה {elapsed:.3f}s עולה על המקסימום {MAX_RESPONSE_TIME}s"


@allure.feature("Performance")
class TestMultipleRequestsPerformance:

    @allure.title("10 בקשות רצופות - ממוצע זמני תגובה")
    @allure.severity(allure.severity_level.NORMAL)
    def test_average_response_time(self, api_client):
        times = []
        num_requests = 10

        with allure.step(f"שולח {num_requests} בקשות רצופות"):
            for i in range(num_requests):
                response = api_client.get(f"/posts/{i + 1}")
                times.append(response.elapsed.total_seconds())

        with allure.step("מחשב סטטיסטיקות"):
            avg_time = statistics.mean(times)
            max_time = max(times)
            min_time = min(times)

            allure.attach(
                f"ממוצע: {avg_time:.3f}s\n"
                f"מקסימום: {max_time:.3f}s\n"
                f"מינימום: {min_time:.3f}s",
                name="Response Time Statistics",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step(f"מוודא שהממוצע קטן מ־{ACCEPTABLE_RESPONSE_TIME} שניות"):
            assert avg_time < ACCEPTABLE_RESPONSE_TIME, \
                f"ממוצע זמן תגובה {avg_time:.3f}s עולה על המקסימום"

    @allure.title("בדיקת עקביות - סטיית תקן זמני תגובה")
    @allure.severity(allure.severity_level.MINOR)
    def test_response_time_consistency(self, api_client):
        times = []
        num_requests = 5

        with allure.step(f"שולח {num_requests} בקשות זהות"):
            for _ in range(num_requests):
                response = api_client.get("/posts/1")
                times.append(response.elapsed.total_seconds())

        with allure.step("מחשב סטיית תקן"):
            std_dev = statistics.stdev(times)

            allure.attach(
                f"זמנים: {[f'{t:.3f}s' for t in times]}\n"
                f"סטיית תקן: {std_dev:.3f}s",
                name="Consistency Statistics",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("מוודא שסטיית התקן קטנה מ־0.5 שניות"):
            assert std_dev < 0.5, \
                f"סטיית תקן {std_dev:.3f}s גדולה מדי — תגובות לא עקביות"


@allure.feature("Performance")
class TestConcurrentRequests:

    @allure.title("בקשות מקבילות - זמן כולל")
    @allure.severity(allure.severity_level.NORMAL)
    def test_concurrent_requests_total_time(self, api_client):
        import threading
        results = []
        num_threads = 5

        def make_request(post_id):
            response = api_client.get(f"/posts/{post_id}")
            results.append({
                "post_id": post_id,
                "status": response.status_code,
                "time": response.elapsed.total_seconds()
            })

        with allure.step(f"שולח {num_threads} בקשות מקבילות"):
            start_time = time.time()

            threads = [
                threading.Thread(target=make_request, args=(i + 1,))
                for i in range(num_threads)
            ]

            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            total_time = time.time() - start_time

        with allure.step("מוודא שכל הבקשות הצליחו"):
            allure.attach(
                f"זמן כולל: {total_time:.3f}s\n"
                f"תוצאות: {results}",
                name="Concurrent Results",
                attachment_type=allure.attachment_type.TEXT
            )

            assert len(results) == num_threads
            for result in results:
                assert result["status"] == 200