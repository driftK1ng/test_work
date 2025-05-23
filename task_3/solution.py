def appearance(intervals: dict[str, list[int]]) -> int:
    """Исправляет интервалы и производит вычисление пересекающихся интервалов пользователей

    Args:
        intervals (dict[str, list[int]]): Исходные интервалы

    Returns:
        int: Суммарное время
    """
    intervals['pupil'] = normalize_activity(intervals['pupil'])
    intervals['tutor'] = normalize_activity(intervals['tutor'])
    intervals['pupil'] = intervals_cut_lesson(intervals['pupil'], intervals['lesson'])
    intervals['tutor'] = intervals_cut_lesson(intervals['tutor'], intervals['lesson'])
    timeline = form_timeline(intervals['pupil'], intervals['tutor'])
    return compare_interval(timeline)

def intervals_cut_lesson(intervals: list[int], lesson_interval: list[int]) -> list[int]:
    """Если интервал начинается или заканчивается до урока,
     то устанавливает начало/конец интервала к началу/концу урока

    Args:
        intervals (list[int]): Интервалы которые требуется проверить на соответствие интервалу урока
        lesson_interval (list[int]): Интервал урока

    Returns:
        list[int]: Итоговые интервалы
    """
    new_intervals = []
    for index in range(0, len(intervals)-1, 2):
        start, end = intervals[index], intervals[index+1]
        start = max(start, lesson_interval[0])
        end = min(end, lesson_interval[1])
        new_intervals.append(start)
        new_intervals.append(end)
    return new_intervals

def normalize_activity(interval: list[int]) -> list[int]:
    """Формирует из пересекающихся интервалов, один интервал

    Args:
        interval (list[int]): Интервалы, в которых нужно убрать пересечения

    Returns:
        list[int]: Итоговые интервалы 
    """
    timeline = {}
    for index in range(0, len(interval)-1, 2):
        timeline[f"start_{index}"] = interval[index]
        timeline[f"end_{index}"] = interval[index+1]
    timeline = (dict(sorted(timeline.items(), key=lambda item: item[1])))
    active_intervals = []
    right_intervals = []
    start_time = None
    for key, value in timeline.items():
        if key.split("_")[0] == "start" and key.split("_")[1] not in active_intervals:
            active_intervals.append(key.split("_")[1])
            if start_time is None:
                start_time = value
        elif key.split("_")[0] == "end" and key.split("_")[1] in active_intervals:
            active_intervals.remove(key.split("_")[1])
            if len(active_intervals) == 0:
                right_intervals.append(start_time)
                right_intervals.append(value)
                start_time = None
    return right_intervals

def form_timeline(pupil_interval: list[int], tutor_interval: list[int]) -> dict[str, int]:
    """Формирует словарь обьединенных действий пользователей

    Args:
        pupil_interval (list[int]): Интервалы ученика
        tutor_interval (list[int]): Интервалы учителя

    Returns:
        dict[str,int]: Словарь действий пользователей
    """
    timeline = {}
    for index in range(0, len(pupil_interval) - 1, 2):
        timeline[f"p_start_{index}"] = pupil_interval[index]
        timeline[f"p_end_{index}"] = pupil_interval[index+1]
    for index in range(0, len(tutor_interval) - 1, 2):
        timeline[f"t_start_{index}"] = tutor_interval[index]
        timeline[f"t_end_{index}"] = tutor_interval[index+1]
    return (dict(sorted(timeline.items(), key=lambda item: item[1])))

def compare_interval(timeline: dict) -> int:
    """Проходится по словарю действий пользователей и получает суммарное время 
    одновременно открытых сессий пользователей

    Args:
        timeline (dict): Словарь действий пользователей

    Returns:
        int: Суммарное количество времени одновременных сессий
    """
    summ = 0
    in_interval = False
    start_time = -1
    for key, value in timeline.items():
        if (key.split("_"))[1] == "start":
            if (in_interval) is False:
                in_interval = True
            else:
                start_time = value
        if (key.split("_"))[1] == "end":
            if (start_time) != -1:
                summ += value - start_time
                start_time = -1
            else:
                in_interval = False
    return summ

