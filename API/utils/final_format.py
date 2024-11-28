debug_mode = True

def compute_and_segment(data):
    """ Method for segments the input data based on labels, 
        calculates start times and durations for each segment, 
        estimating timestamps from a B-X position, 
        return a data structure organized by events """
    print("\nProcessing Format in progress...\n")

    def log(message):
        if debug_mode and item_index < 50:
            print(message)

    output_data = []
    item_index = 0

    for item in data:
        time_start = item['time_start']
        time_end = item['time_end']
        words = item['words']
        labels = item['labels']
        number_of_words = len(words)
        total_duration = time_end - time_start

        log(f"\n- Original text: '{item['text']}'")
        log(f"- Timeframe: {time_start} to {time_end} with {number_of_words} words")
        log(f"- Total duration: {total_duration} seconds")

        # estimate the duration per word
        duration_per_word = total_duration / number_of_words

        # calculate per-word start times (and add an extra point for the end time)
        per_word_times = [round(time_start + i * duration_per_word, 2) for i in range(number_of_words + 1)]
        log(f"- Times for each word: {per_word_times}")

        # initialize variables for segmenting
        event_segments = []
        current_event = None
        current_segment = None

        # loop through each label to identify segments
        for i in range(len(labels)):
            label = labels[i]
            if label == 'O':
                event = 'O'
            elif label.startswith('B-'):
                event = label[2:]
            elif label.startswith('I-'):
                event = current_event
            else:
                event = 'O'

            # start a new segment if the event changes
            if event != current_event:
                if current_segment is not None:
                    current_segment['end_index'] = i
                    event_segments.append(current_segment)
                    log(f"- Closed segment for '{current_event}' spanning from index {current_segment['start_index']} to {i}")

                current_segment = {'start_index': i, 'event': event}
                current_event = event
                log(f"- Started new segment for '{event}' at index {i}")

        # add the last segment
        if current_segment is not None:
            current_segment['end_index'] = len(labels)
            event_segments.append(current_segment)
            log(f"- Added final segment for '{current_event}' from index {current_segment['start_index']} to {len(labels)}")

        # compute the start time and duration for each segment
        for segment in event_segments:
            start_index = segment['start_index']
            end_index = segment['end_index']
            event = segment['event']
            segment_start_time = per_word_times[start_index]
            segment_end_time = per_word_times[end_index]
            duration = segment_end_time - segment_start_time
 
            segment_start_time = round(segment_start_time, 2) # Round 2 decimal
            duration = round(duration, 2)

            words_segment = words[start_index:end_index]
            labels_segment = labels[start_index:end_index]
            output_segment = {
                'start_time': segment_start_time,
                'duration': duration,
                'words': words_segment,
                'labels': labels_segment,
                'event': event
            }
            output_data.append(output_segment)
            log(f"- Segment details - [ event: {event}, start_time: {segment_start_time}, duration: {duration} ]")
            log(f"  Words: {words_segment}")
            log(f"  Labels: {labels_segment}")

        item_index += 1
    print("\nFormat processing completed\n")
    return output_data