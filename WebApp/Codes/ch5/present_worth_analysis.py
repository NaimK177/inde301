from manimlib import *
import numpy as np

class PresentWorthAnalysis(Scene):
    def construct(self):
        # ----------------------------------------------------
        # 1. HEADER & TITLE (Static - no animation)
        # ----------------------------------------------------
        title = Text("Present Worth (PW) Analysis", font_size=40)
        title.to_edge(UP, buff=0.4)
        
        subtitle = Text("Discounting future cash flows to the present at MARR", font_size=22, color=GREY_A)
        subtitle.next_to(title, DOWN, buff=0.15)
        
        # Added statically as requested
        self.add(title, subtitle)
        self.wait(0.5)

        # ----------------------------------------------------
        # 2. TIMELINES SETUP (No numbers)
        # ----------------------------------------------------
        y_A = 1.2
        y_B = -1.8
        
        timeline_A = NumberLine(x_range=[0, 3, 1], width=7.5, include_numbers=False)
        timeline_A.move_to(np.array([0.5, y_A, 0]))
        
        timeline_B = NumberLine(x_range=[0, 3, 1], width=7.5, include_numbers=False)
        timeline_B.move_to(np.array([0.5, y_B, 0]))
        
        # Labels for Alternatives
        label_A = Text("Alternative A", font_size=26, color=TEAL).next_to(timeline_A, LEFT, buff=0.4)
        label_B = Text("Alternative B", font_size=26, color=ORANGE).next_to(timeline_B, LEFT, buff=0.4)

        # Tick marks (no numbers)
        ticks_A = VGroup()
        ticks_B = VGroup()

        for t in range(4):
            pt_a = timeline_A.number_to_point(t)
            ticks_A.add(Line(UP * 0.15, DOWN * 0.15).move_to(pt_a))

            pt_b = timeline_B.number_to_point(t)
            ticks_B.add(Line(UP * 0.15, DOWN * 0.15).move_to(pt_b))

        self.play(
            ShowCreation(timeline_A), ShowCreation(ticks_A), Write(label_A),
            ShowCreation(timeline_B), ShowCreation(ticks_B), Write(label_B),
            run_time=1.2
        )

        # ----------------------------------------------------
        # 3. CASH FLOW ARROWS (Sequential: Outlay first, then Inflows)
        # ----------------------------------------------------
        # Alternative A Cash Flows (Teal theme)
        outlay_A_height = 1.00
        inflows_A_heights = [0.60, 0.60, 0.60]

        pt_A_0 = timeline_A.number_to_point(0)
        arrow_out_A = Arrow(pt_A_0, pt_A_0 + DOWN * outlay_A_height, buff=0, stroke_width=4).set_color(TEAL_E)
        
        arrows_in_A = VGroup()
        for t in range(1, 4):
            pt = timeline_A.number_to_point(t)
            arr = Arrow(pt, pt + UP * inflows_A_heights[t-1], buff=0, stroke_width=4).set_color(TEAL)
            arrows_in_A.add(arr)

        # Alternative B Cash Flows (Orange theme)
        outlay_B_height = 1.20
        inflows_B_heights = [0.40, 0.70, 0.90]

        pt_B_0 = timeline_B.number_to_point(0)
        arrow_out_B = Arrow(pt_B_0, pt_B_0 + DOWN * outlay_B_height, buff=0, stroke_width=4).set_color(ORANGE)
        
        arrows_in_B = VGroup()
        for t in range(1, 4):
            pt = timeline_B.number_to_point(t)
            arr = Arrow(pt, pt + UP * inflows_B_heights[t-1], buff=0, stroke_width=4).set_color(GOLD)
            arrows_in_B.add(arr)

        # Step 3a: Show Initial Outlays at t=0 first
        self.play(
            GrowArrow(arrow_out_A),
            GrowArrow(arrow_out_B),
            run_time=1.0
        )
        self.wait(0.8)

        # Step 3b: Show Positive Cash Inflows (upward arrows) next
        self.play(
            *[GrowArrow(a) for a in arrows_in_A],
            *[GrowArrow(a) for a in arrows_in_B],
            run_time=1.2
        )
        self.wait(1.0)

        # ----------------------------------------------------
        # 4. EQUIVALENCE / DISCOUNTING ANIMATION
        # ----------------------------------------------------
        disc_banner = Text("Apply Equivalence: Discounting to Present", font_size=24, color=YELLOW)
        disc_banner.move_to(np.array([0.5, 0.0, 0]))
        self.play(FadeIn(disc_banner, scale=0.9))
        self.wait(0.5)

        # Calculated discount factors (i = 0.10): t=1: 0.91, t=2: 0.83, t=3: 0.75
        discount_factors = [0.9091, 0.8264, 0.7513]

        discounted_A = VGroup()
        discounted_B = VGroup()
        animations = []

        # Background copies for future arrows as faded outlines
        faded_A = arrows_in_A.copy().set_opacity(0.3)
        faded_B = arrows_in_B.copy().set_opacity(0.3)
        self.add(faded_A, faded_B)

        for idx in range(3):
            factor = discount_factors[idx]

            # Alt A arrow move & scale
            orig_arr_A = arrows_in_A[idx]
            new_height_A = inflows_A_heights[idx] * factor
            target_arr_A = Arrow(pt_A_0, pt_A_0 + UP * new_height_A, buff=0, stroke_width=4).set_color(TEAL_A)
            animations.append(ReplacementTransform(orig_arr_A, target_arr_A, path_arc=-0.6))
            discounted_A.add(target_arr_A)

            # Alt B arrow move & scale
            orig_arr_B = arrows_in_B[idx]
            new_height_B = inflows_B_heights[idx] * factor
            target_arr_B = Arrow(pt_B_0, pt_B_0 + UP * new_height_B, buff=0, stroke_width=4).set_color(YELLOW_A)
            animations.append(ReplacementTransform(orig_arr_B, target_arr_B, path_arc=-0.6))
            discounted_B.add(target_arr_B)

        self.play(*animations, run_time=2.5)
        self.wait(1.0)

        # ----------------------------------------------------
        # 5. NET PRESENT WORTH AT t = 0 (No numbers)
        # ----------------------------------------------------
        pw_in_A_val = sum([inflows_A_heights[i] * discount_factors[i] for i in range(3)])
        pw_net_A_val = pw_in_A_val - outlay_A_height

        pw_in_B_val = sum([inflows_B_heights[i] * discount_factors[i] for i in range(3)])
        pw_net_B_val = pw_in_B_val - outlay_B_height

        # Net Present Worth Arrows (labeled simply PW_A and PW_B with no numbers)
        pw_arrow_A = Arrow(pt_A_0, pt_A_0 + UP * pw_net_A_val, buff=0, stroke_width=6).set_color(GREEN_C)
        pw_label_A = Text("PW_A", font_size=22, color=GREEN_C).next_to(pw_arrow_A, UP + RIGHT, buff=0.1)

        pw_arrow_B = Arrow(pt_B_0, pt_B_0 + UP * pw_net_B_val, buff=0, stroke_width=6).set_color(GREEN_C)
        pw_label_B = Text("PW_B", font_size=22, color=GREEN_C).next_to(pw_arrow_B, UP + RIGHT, buff=0.1)

        summary_text = Text("Equivalent Present Worth at Present", font_size=26, color=GREEN_C)
        summary_text.move_to(disc_banner.get_center())

        self.play(
            ReplacementTransform(disc_banner, summary_text),
            FadeOut(discounted_A), FadeOut(arrow_out_A),
            FadeOut(discounted_B), FadeOut(arrow_out_B),
            GrowArrow(pw_arrow_A), Write(pw_label_A),
            GrowArrow(pw_arrow_B), Write(pw_label_B),
            run_time=2.0
        )

        self.wait(2.0)

