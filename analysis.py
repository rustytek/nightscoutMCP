from typing import List, Dict, Any

def calculate_statistics(entries: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate basic statistics from glucose entries.
    Assumes entries have a 'sgv' (Sensor Glucose Value) field.
    """
    if not entries:
        return {
            "average_glucose": None,
            "time_in_range": 0,
            "entry_count": 0
        }

    valid_entries = [e for e in entries if 'sgv' in e]
    if not valid_entries:
         return {
            "average_glucose": None,
            "time_in_range": 0,
            "entry_count": 0
        }

    total_glucose = sum(e['sgv'] for e in valid_entries)
    avg_glucose = total_glucose / len(valid_entries)

    # Time in Range (70-180 mg/dL)
    in_range_count = sum(1 for e in valid_entries if 70 <= e['sgv'] <= 180)
    tir = (in_range_count / len(valid_entries)) * 100

    return {
        "average_glucose": round(avg_glucose, 1),
        "time_in_range": round(tir, 1),
        "entry_count": len(valid_entries)
    }

def analyze_settings(profile: Dict[str, Any], entries: List[Dict[str, Any]], treatments: List[Dict[str, Any]], device_statuses: List[Dict[str, Any]] = []) -> List[str]:
    """
    Analyze data and suggest setting changes.
    This is a basic heuristic V1.
    """
    stats = calculate_statistics(entries)
    suggestions = []

    avg_glucose = stats.get("average_glucose")
    tir = stats.get("time_in_range")

    if avg_glucose is None:
        return ["Not enough data to make suggestions."]

    suggestions.append(f"Analysis based on {stats['entry_count']} entries covering approximately {stats['entry_count'] * 5 / 60:.1f} hours.")
    suggestions.append(f"Current Statistics: Average Glucose {avg_glucose} mg/dL, Time in Range {tir}%.")

    # Loop Data Analysis
    loop_statuses = [ds['loop'] for ds in device_statuses if 'loop' in ds]
    if loop_statuses:
        avg_iob = sum(s.get('iob', {}).get('iob', 0) for s in loop_statuses) / len(loop_statuses)
        avg_cob = sum(s.get('cob', {}).get('cob', 0) for s in loop_statuses) / len(loop_statuses)
        suggestions.append(f"Loop Data Analysis ({len(loop_statuses)} records): Avg IOB {avg_iob:.2f} U, Avg COB {avg_cob:.1f} g.")
        
        # Heuristic: High Glucose + High IOB = Insulin resistance or bad site?
        if avg_glucose > 160 and avg_iob > 1.0: # Thresholds are arbitrary illustrative examples
             suggestions.append("High average glucose with active insulin (IOB) present. Consider checking specifically for post-prandial spikes or checking your ISF if highs persist with IOB.")

    # Basic Heuristics
    if avg_glucose > 160:
        suggestions.append("High average glucose detected (> 160 mg/dL). Consider increasing basal rates or Aggressive Factor (ISF).")
    elif avg_glucose < 100:
        suggestions.append("Low average glucose detected (< 100 mg/dL). Consider decreasing basal rates or making ISF less aggressive.")
    
    if tir < 70:
        suggestions.append("Time in Range is below 70%. clearer identification of patterns (high/low) is needed to adjust specific settings.")

    return suggestions
