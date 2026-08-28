from manimlib import *

class IPhoneEquivalence(Scene):
    def construct(self):
        # ----------------------------------------------------
        # SCENE SETUP
        # ----------------------------------------------------
        title = Text("Economic Equivalence: iPhone Purchase\n Present Worth Analysis", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Timeline setup
        timeline = NumberLine(
            x_range=[-1, 2, 1],
            width=10,
            include_numbers=False
        )
        timeline.shift(DOWN * 1.5)
        
        # Define Year 0 and Year 1 positions
        t0_point = timeline.number_to_point(0)
        t1_point = timeline.number_to_point(1)
        
        # Add ticks
        t0_tick = Line(UP * 0.2, DOWN * 0.2).move_to(t0_point)
        t1_tick = Line(UP * 0.2, DOWN * 0.2).move_to(t1_point)
        
        # Add labels for timeline
        t0_label = Text("Year 0 (Now)", font_size=24).next_to(t0_tick, DOWN)
        t1_label = Text("Year 1 (Next Year)", font_size=24).next_to(t1_tick, DOWN)
        
        self.play(
            ShowCreation(timeline),
            ShowCreation(t0_tick), ShowCreation(t1_tick),
            Write(t0_label), Write(t1_label)
        )
        
        # Show Interest Rate
        rate_text = Text("Interest Rate: 6%", font_size=36).set_color(YELLOW)
        rate_text.to_edge(DOWN)
        self.play(Write(rate_text))
        
        # ----------------------------------------------------
        # PRESENT WORTH ANALYSIS 
        # ----------------------------------------------------
        # pw_title = Text("Present Worth Analysis", font_size=36, color=BLUE)
        # pw_title.next_to(rate_text, DOWN, buff=0.5).align_to(title, LEFT)
        # self.play(Write(pw_title))
        
        # Option A: Buy Now ($1100) - Colored GREEN
        optA_arrow = Arrow(start=t0_point + LEFT * 0.05, end=t0_point + LEFT * 0.05 + UP * 2.2, buff=0).set_color(GREEN)
        optA_text = Text("Option A: Buy Now", font_size=24)
        optA_val = Text("$1100", font_size=36).set_color(GREEN)
        optA_group = VGroup(optA_text, optA_val).arrange(DOWN)
        optA_group.next_to(optA_arrow, UP + LEFT, buff=0.2)
        
        # Option B: Buy Next Year ($1200) - Colored RED
        optB_arrow = Arrow(start=t1_point, end=t1_point + UP * 2.4, buff=0).set_color(RED)
        optB_text = Text("Option B: Buy Next Year", font_size=24)
        optB_val = Text("$1200", font_size=36).set_color(RED)
        optB_group = VGroup(optB_text, optB_val).arrange(DOWN)
        optB_group.next_to(optB_arrow, UP + RIGHT, buff=0.2)
        
        self.play(
            # GrowArrow(optA_arrow), FadeIn(optA_group),
            GrowArrow(optB_arrow), FadeIn(optB_group)
        )
        self.wait(1)
        

        
        # MOVING ARROW & TEXT SETUP (Dynamic)
        moving_val_tracker = ValueTracker(1200)
        
        def update_optB_arrow(arr):
            val = moving_val_tracker.get_value()
            alpha = (1200 - val) / (1200 - 1132) if val <= 1200 else 0
            current_base = t1_point * (1 - alpha) + (t0_point + RIGHT * 0.05) * alpha
            arrow_length = val * 0.002
            new_arrow = Arrow(start=current_base, end=current_base + UP * arrow_length, buff=0).set_color(RED)
            arr.become(new_arrow)
            
        def update_optB_group(grp):
            val = int(moving_val_tracker.get_value())
            alpha = (1200 - val) / (1200 - 1132) if val <= 1200 else 0
            current_base = t1_point * (1 - alpha) + (t0_point + RIGHT * 0.05) * alpha
            arrow_length = moving_val_tracker.get_value() * 0.002
            
            text = Text("Option B: Buy Next Year", font_size=24)
            val_text = Text(f"${val}", font_size=36).set_color(RED)
            new_group = VGroup(text, val_text).arrange(DOWN)
            new_group.next_to(current_base + UP * arrow_length, UP + RIGHT, buff=0.2)
            grp.become(new_group)

        optB_arrow.add_updater(update_optB_arrow)
        optB_group.add_updater(update_optB_group)
        
        # Animate the value discounting AND the arrow moving/shrinking simultaneously!
        self.play(
            moving_val_tracker.animate.set_value(1132),
            run_time=4.5,
            rate_func=smooth
        )
        self.wait(0.5)
        
        optB_arrow.remove_updater(update_optB_arrow)
        optB_group.remove_updater(update_optB_group)
        
        # not needed
        # pw_eq_label = Text("Equivalent at Year 0", font_size=20, color=RED)
        # pw_eq_label.next_to(optB_group, UP)
        # self.play(Write(pw_eq_label))
        # Add here a zoom in to the time 0, and afterwards the arrow of option 1 
        # to make the comparison more clear
        zoom_target = t0_point + UP * 1.5  # Center around the arrows
        self.play(
            self.camera.frame.animate.set_width(8).move_to(zoom_target),
            run_time=1.5
        )
        self.wait(0.5)
        
        self.play(
            GrowArrow(optA_arrow), FadeIn(optA_group)
        )
        self.wait(1)

        # Compare Option A to Option B's equivalent
        compare_pw = Text("$1132 > $1100. Save $32 by buying now!", font_size=30).set_color(GREEN)
        # Position this relative to the optB_group since pw_eq_label was removed
        compare_pw.next_to(optB_group, UP, buff=1.0)
        self.play(Write(compare_pw))
        self.wait(4)
