```

## 👤 USERS

### 1. GET /users

Возвращает:

* список пользователей
* пагинация
* количество каналов у каждого user (annotate)

---

### 2. POST /users

Создаёт пользователя
Возвращает:

* user данные
* id

---

### 3. GET /users/{id}

Возвращает:

* user
* список каналов (nested)
* общее количество видео во всех каналах

---

### 4. GET /users/{id}/channels

Возвращает:

* каналы пользователя
* количество видео в каждом канале

---

---

## 📺 CHANNELS

### 5. GET /channels

Возвращает:

* список каналов
* owner (nested user)
* subscribers_count (аннотированное поле)

---

### 6. POST /channels

Создаёт канал
Возвращает:

* канал
* owner
* пустая статистика

---

### 7. GET /channels/{id}

Возвращает:

* канал
* owner
* последние 5 видео
* total views (aggregate)

---

### 8. PUT /channels/{id}

Обновляет канал
Возвращает:

* обновлённый объект
* флаг "updated=True"

---

### 9. DELETE /channels/{id}

Удаляет канал
Возвращает:

* status
* deleted channel id

---

### 10. GET /channels/{id}/videos

Возвращает:

* видео канала
* сортировка: latest / popular
* фильтр по date range

---

### 11. GET /channels/{id}/stats

Возвращает:

* total videos
* total views
* avg views per video
* top video

---

---

## 🎬 VIDEOS

### 12. GET /videos

Возвращает:

* список видео
* channel nested 
* pagination 
* search + filter + ordering

---

### 13. POST /videos

Создаёт видео
Возвращает:

* видео
* автоматически views = 0 
* channel info 

---

### 14. GET /videos/{id}

Возвращает:

* видео
* channel
* comments_count
* likes_count
* views++ (side effect)

---














### 15. PUT /videos/{id}

Обновляет видео
Возвращает:

* updated object
* diff changes (old vs new) ##################

---

### 16. DELETE /videos/{id}

Удаляет видео
Возвращает:

* status
* cascade delete info (comments, likes)

---

---

## 💬 COMMENTS

### 17. GET /videos/{id}/comments

Возвращает:

* список комментариев
* user nested
* pagination
* sorting (new/old/popular)

---

### 18. POST /videos/{id}/comments

Создаёт комментарий
Возвращает:

* comment
* user
* video_id

---

### 19. GET /comments/{id}

Возвращает:

* comment
* user
* video info

---

### 20. DELETE /comments/{id}

Возвращает:

* status
* deleted comment id

---

---

## 👍 LIKES

### 21. POST /videos/{id}/like

Логика:

* если лайка нет → создать
* если есть → ошибка или toggle

Возвращает:

* liked=True
* total likes

---

### 22. DELETE /videos/{id}/like

Возвращает:

* liked=False
* total likes

---

### 23. GET /videos/{id}/likes

Возвращает:

* список пользователей
* total count
* is_liked_by_current_user (fake user_id) ##################

---

---

## 🔍 SEARCH / FILTER 

### 24. GET /videos/search?query=

Возвращает:

* поиск по title + description
* ranking (relevance score) ##################

---

### 25. GET /videos?channel={id}

Возвращает:

* видео конкретного канала
* ordered by views

---



########################################################################



### 26. GET /videos/top

Возвращает:

* топ 10 видео
* сортировка по views
* optional time filter (day/week/month)

---

### 27. GET /videos/{id}/related

Возвращает:

* похожие видео
* based on title similarity / channel

---

---

## 📊 STATS

### 28. GET /stats/videos

Возвращает:

* total videos
* total views
* avg views

---

### 29. GET /stats/users

Возвращает:

* total users
* users with channels
* active users (fake logic)

---

### 30. GET /stats/channels

Возвращает:

* total channels
* top channel by views
* average videos per channel

 ```
