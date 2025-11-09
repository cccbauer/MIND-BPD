#!/usr/bin/env python3
"""
Diagnostic script to understand why SHAM isn't getting virtual hits

Usage:
    python diagnose_sham_hits.py --participant 2099 --run 1
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def diagnose_sham_virtual_hits(participant_id, run_number):
    """Diagnose why SHAM isn't getting virtual hits"""
    
    # Load data
    filepath = f'data/sub-mindbpd{participant_id}/sub-mindbpd{participant_id}_DMN_feedback_{run_number}_roi_outputs.csv'
    
    print(f"\n{'='*70}")
    print(f"Diagnosing SHAM Virtual Hits for Participant {participant_id}, Run {run_number}")
    print(f"{'='*70}\n")
    
    try:
        df = pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"ERROR: File not found: {filepath}")
        return
    
    # Filter to feedback period
    df_fb = df[df['stage'] == 'feedback'].copy()
    
    print(f"Total volumes: {len(df)}")
    print(f"Feedback volumes: {len(df_fb)}")
    print(f"\nBrain Activity Statistics:")
    print(f"  CEN - Mean: {df_fb['cen'].mean():.4f}, Std: {df_fb['cen'].std():.4f}, Min: {df_fb['cen'].min():.4f}, Max: {df_fb['cen'].max():.4f}")
    print(f"  DMN - Mean: {df_fb['dmn'].mean():.4f}, Std: {df_fb['dmn'].std():.4f}, Min: {df_fb['dmn'].min():.4f}, Max: {df_fb['dmn'].max():.4f}")
    
    # Check current hit counts
    print(f"\nRecorded Hit Counts:")
    print(f"  CEN hits: {df_fb['cen_cumulative_hits'].max()}")
    print(f"  DMN hits: {df_fb['dmn_cumulative_hits'].max()}")
    
    # Simulate virtual ball movement
    scale_factor = 10
    internal_scaler = 10
    tr = 1.2
    frame_rate = 60.0
    tr_to_frame_ratio = tr / (1.0 / frame_rate)
    pda_outlier_threshold = 2
    positions = [1, -1]  # CEN=1, DMN=-1
    
    # Get target positions
    if 'top_circle_y_position' in df_fb.columns and 'bottom_circle_y_position' in df_fb.columns:
        top_target = df_fb['top_circle_y_position'].iloc[0]
        bottom_target = df_fb['bottom_circle_y_position'].iloc[0]
    else:
        top_target = 0.33
        bottom_target = -0.33
    
    print(f"\nTarget Positions:")
    print(f"  CEN (top): {top_target:.4f}")
    print(f"  DMN (bottom): {bottom_target:.4f}")
    print(f"\nSimulating Virtual Ball Movement...")
    print(f"  Scale factor: {scale_factor}")
    print(f"  Internal scaler: {internal_scaler}")
    print(f"  TR to frame ratio: {tr_to_frame_ratio:.2f}")
    
    # Simulate
    virtual_cen_hits = 0
    virtual_dmn_hits = 0
    virtual_ball_y = 0.0
    
    ball_positions = []
    hit_volumes = []
    
    for idx, row in df_fb.iterrows():
        cen_val = row['cen']
        dmn_val = row['dmn']
        volume = row['volume']
        
        if pd.isna(cen_val) or pd.isna(dmn_val):
            ball_positions.append(virtual_ball_y)
            continue
        
        roi_activities = [cen_val, dmn_val]
        
        # Check for outlier
        if np.max(np.abs(roi_activities)) > pda_outlier_threshold:
            pda_outlier = True
        else:
            pda_outlier = False
        
        # Calculate virtual ball movement
        if not pda_outlier and np.mean(roi_activities) != 0:
            max_roi_idx = roi_activities.index(np.max(roi_activities))
            activity = abs(np.max(roi_activities) - np.min(roi_activities)) / 10
            direction = positions[max_roi_idx]
            
            # Calculate movement per frame (matching REAL mode exactly)
            cursor_position = direction * activity
            num_frames_per_tr = int(tr_to_frame_ratio)
            delta_per_frame = (cursor_position * (scale_factor/internal_scaler) / tr_to_frame_ratio)
            
            # Simulate frame-by-frame updates within this TR
            for frame_idx in range(num_frames_per_tr):
                virtual_ball_y += delta_per_frame
                
                # Check for hits after each simulated frame
                if virtual_ball_y > top_target:
                    virtual_cen_hits += 1
                    hit_volumes.append((volume, 'CEN', virtual_ball_y))
                    print(f"  Volume {volume}: VIRTUAL CEN HIT (ball_y={virtual_ball_y:.4f}, frame={frame_idx}/{num_frames_per_tr}, CEN={cen_val:.4f}, DMN={dmn_val:.4f})")
                    virtual_ball_y = 0.0
                    break
                elif virtual_ball_y < bottom_target:
                    virtual_dmn_hits += 1
                    hit_volumes.append((volume, 'DMN', virtual_ball_y))
                    print(f"  Volume {volume}: VIRTUAL DMN HIT (ball_y={virtual_ball_y:.4f}, frame={frame_idx}/{num_frames_per_tr}, CEN={cen_val:.4f}, DMN={dmn_val:.4f})")
                    virtual_ball_y = 0.0
                    break
        
        ball_positions.append(virtual_ball_y)
    
    print(f"\n{'='*70}")
    print(f"SIMULATION RESULTS:")
    print(f"  Virtual CEN hits: {virtual_cen_hits}")
    print(f"  Virtual DMN hits: {virtual_dmn_hits}")
    print(f"  Total virtual hits: {virtual_cen_hits + virtual_dmn_hits}")
    print(f"{'='*70}\n")
    
    # Additional diagnostics
    print("DIAGNOSTIC CHECKS:")
    
    # Check if brain activity is strong enough
    pda = df_fb['cen'] - df_fb['dmn']
    print(f"  PDA (CEN - DMN) - Mean: {pda.mean():.4f}, Max: {pda.max():.4f}, Min: {pda.min():.4f}")
    
    # Check outliers
    outliers = (np.abs(df_fb['cen']) > pda_outlier_threshold) | (np.abs(df_fb['dmn']) > pda_outlier_threshold)
    print(f"  Outlier volumes: {outliers.sum()} / {len(df_fb)} ({100*outliers.sum()/len(df_fb):.1f}%)")
    
    # Check if ball ever got close to targets
    max_ball_y = max(ball_positions)
    min_ball_y = min(ball_positions)
    print(f"  Max ball position reached: {max_ball_y:.4f} (target: {top_target:.4f})")
    print(f"  Min ball position reached: {min_ball_y:.4f} (target: {bottom_target:.4f})")
    print(f"  Distance from CEN target: {abs(max_ball_y - top_target):.4f}")
    print(f"  Distance from DMN target: {abs(min_ball_y - bottom_target):.4f}")
    
    # Create visualization
    fig, axes = plt.subplots(3, 1, figsize=(14, 10))
    
    # Plot 1: Virtual ball position over time
    axes[0].plot(df_fb['volume'], ball_positions, linewidth=2, color='blue')
    axes[0].axhline(y=top_target, color='orange', linestyle='--', label=f'CEN Target ({top_target:.2f})')
    axes[0].axhline(y=bottom_target, color='cyan', linestyle='--', label=f'DMN Target ({bottom_target:.2f})')
    axes[0].axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    axes[0].set_ylabel('Virtual Ball Y Position', fontweight='bold')
    axes[0].set_title(f'SHAM {participant_id} - Simulated Virtual Ball Movement', fontweight='bold')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Mark hits
    for vol, hit_type, pos in hit_volumes:
        color = 'orange' if hit_type == 'CEN' else 'cyan'
        axes[0].scatter(vol, pos, color=color, s=100, marker='*', zorder=5)
    
    # Plot 2: Brain activity
    axes[1].plot(df_fb['volume'], df_fb['cen'], linewidth=2, color='orange', label='CEN', alpha=0.8)
    axes[1].plot(df_fb['volume'], df_fb['dmn'], linewidth=2, color='cyan', label='DMN', alpha=0.8)
    axes[1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
    axes[1].axhline(y=pda_outlier_threshold, color='red', linestyle=':', alpha=0.5, label='Outlier threshold')
    axes[1].axhline(y=-pda_outlier_threshold, color='red', linestyle=':', alpha=0.5)
    axes[1].set_ylabel('Activation (z-score)', fontweight='bold')
    axes[1].set_title('Brain Activity (CEN vs DMN)', fontweight='bold')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    # Plot 3: PDA
    axes[2].plot(df_fb['volume'], pda, linewidth=2, color='purple', alpha=0.8)
    axes[2].axhline(y=0, color='black', linestyle='-', alpha=0.5)
    axes[2].fill_between(df_fb['volume'], 0, pda, where=(pda > 0), alpha=0.3, color='orange', label='CEN Dominant')
    axes[2].fill_between(df_fb['volume'], 0, pda, where=(pda < 0), alpha=0.3, color='cyan', label='DMN Dominant')
    axes[2].set_xlabel('Volume', fontweight='bold')
    axes[2].set_ylabel('PDA (CEN - DMN)', fontweight='bold')
    axes[2].set_title('Preferential Differential Activation', fontweight='bold')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    output_file = f'sham_{participant_id}_run{run_number}_diagnosis.png'
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"\nDiagnostic plot saved as: {output_file}")
    
    plt.show()
    
    return virtual_cen_hits, virtual_dmn_hits


def main():
    parser = argparse.ArgumentParser(description='Diagnose SHAM virtual hits')
    parser.add_argument('--participant', type=int, required=True, help='Participant ID (e.g., 2099)')
    parser.add_argument('--run', type=int, default=1, help='Run number (default: 1)')
    
    args = parser.parse_args()
    
    diagnose_sham_virtual_hits(args.participant, args.run)


if __name__ == '__main__':
    main()
