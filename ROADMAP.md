# Hutishtuti Poker AI - Development Roadmap

**Project Goal:** Build a complete poker game analyzer that captures all game data from ClubGG offline tables, stores it in CSV format, and uses neural networks to recommend optimal actions.

**Current Status:** ✅ Card OCR detection working

---

## EPIC 1: Enhanced OCR & Data Capture Infrastructure
**Goal:** Expand OCR capabilities to capture all visible table information
**Priority:** HIGH
**Estimated Duration:** 3-4 weeks

### Story 1.1: Player Position Detection [5 Story Points]
**Description:** Detect and track all player positions at the table
**Acceptance Criteria:**
- [ ] Calibrate screen coordinates for all player positions (up to 9 players)
- [ ] OCR reads player names/IDs from each position
- [ ] System tracks which positions are active (seated) vs empty
- [ ] System identifies hero (user's) position
- [ ] Validate detection accuracy >95% on test screenshots

**Technical Tasks:**
- [ ] Extend config.yaml with player_position_locations (9 positions)
- [ ] Create `ocr_player_detector.py` module
- [ ] Add player name OCR with tesseract
- [ ] Implement empty seat detection (color/pattern matching)
- [ ] Add player position calibration to visual calibration tool
- [ ] Write unit tests for player detection

**Dependencies:** None
**Assigned To:** [Team Member]

---

### Story 1.2: Dealer Button Detection [3 Story Points]
**Description:** Detect dealer button location to determine positions (BTN, SB, BB, etc.)
**Acceptance Criteria:**
- [ ] Calibrate screen coordinates for dealer button icon
- [ ] Detect which position has the dealer button
- [ ] Calculate relative positions (UTG, MP, CO, BTN, SB, BB)
- [ ] Handle button movement between hands
- [ ] Validate accuracy >98%

**Technical Tasks:**
- [ ] Add dealer_button_locations to config (9 possible positions)
- [ ] Implement image pattern matching for dealer button icon
- [ ] Create position calculator (UTG+0, UTG+1, etc.)
- [ ] Add dealer button to calibration tool
- [ ] Add logging for dealer position tracking

**Dependencies:** Story 1.1
**Assigned To:** [Team Member]

---

### Story 1.3: Pot Size OCR [3 Story Points]
**Description:** Read and track pot size from screen
**Acceptance Criteria:**
- [ ] Calibrate pot size display location
- [ ] OCR reads pot amount (handle decimal values)
- [ ] Handle different pot displays (main pot, side pots)
- [ ] Parse currency symbols and commas correctly
- [ ] Validate accuracy >99% on numeric values

**Technical Tasks:**
- [ ] Add pot_size_location to config.yaml
- [ ] Create numeric OCR function with preprocessing
- [ ] Handle currency formatting ($, commas, decimals)
- [ ] Add pot size reading to ocr_reader.py
- [ ] Add side pot detection logic
- [ ] Write tests for numeric parsing

**Dependencies:** None
**Assigned To:** [Team Member]

---

### Story 1.4: Player Stack Size OCR [5 Story Points]
**Description:** Read stack sizes for all active players
**Acceptance Criteria:**
- [ ] Calibrate stack display locations for all 9 positions
- [ ] OCR reads numeric stack values
- [ ] Track stack changes throughout hand
- [ ] Handle abbreviations (1.5K, 2.3M)
- [ ] Validate accuracy >95%

**Technical Tasks:**
- [ ] Add player_stack_locations to config (9 positions)
- [ ] Extend numeric OCR for stack parsing
- [ ] Handle abbreviations (K, M suffixes)
- [ ] Create stack tracker class
- [ ] Add to visual calibration tool
- [ ] Write tests for stack tracking

**Dependencies:** Story 1.1
**Assigned To:** [Team Member]

---

### Story 1.5: Bet/Action Amount Detection [5 Story Points]
**Description:** Detect betting amounts and action types for each player
**Acceptance Criteria:**
- [ ] Calibrate bet amount display locations (9 positions)
- [ ] OCR reads bet/raise amounts
- [ ] Detect action types (fold, check, call, bet, raise, all-in)
- [ ] Track bet amounts per betting round
- [ ] Validate accuracy >90%

**Technical Tasks:**
- [ ] Add bet_amount_locations to config (9 positions)
- [ ] Add action_indicator_locations to config
- [ ] Create action detection logic (text + color patterns)
- [ ] Implement bet amount tracking per player
- [ ] Handle multi-street betting
- [ ] Add action detection to calibration tool
- [ ] Write action parser tests

**Dependencies:** Story 1.1, Story 1.4
**Assigned To:** [Team Member]

---

### Story 1.6: Blind Level Detection [2 Story Points]
**Description:** Detect current small blind and big blind amounts
**Acceptance Criteria:**
- [ ] Calibrate blind display location
- [ ] OCR reads SB/BB amounts
- [ ] Track blind level changes
- [ ] Validate accuracy >99%

**Technical Tasks:**
- [ ] Add blind_level_location to config
- [ ] Create blind level parser
- [ ] Add blind tracking to game state
- [ ] Write blind level tests

**Dependencies:** None
**Assigned To:** [Team Member]

---

## EPIC 2: Game State Management & Event Detection
**Goal:** Track complete game state throughout a hand
**Priority:** HIGH
**Estimated Duration:** 2-3 weeks

### Story 2.1: Hand State Machine [8 Story Points]
**Description:** Create comprehensive state machine to track hand progression
**Acceptance Criteria:**
- [ ] State machine tracks: preflop → flop → turn → river → showdown
- [ ] Detect new hand start
- [ ] Detect betting round transitions
- [ ] Track active players per street
- [ ] Handle hand completion/reset

**Technical Tasks:**
- [ ] Create `hand_state_machine.py` module
- [ ] Define state enum (WAITING, PREFLOP, FLOP, TURN, RIVER, SHOWDOWN)
- [ ] Implement state transition logic
- [ ] Add new hand detection (card reset, pot reset)
- [ ] Add betting round completion detection
- [ ] Integrate with existing Game class
- [ ] Write state machine unit tests

**Dependencies:** EPIC 1 stories
**Assigned To:** [Team Member]

---

### Story 2.2: Action Sequence Tracking [5 Story Points]
**Description:** Track all player actions in sequence during a hand
**Acceptance Criteria:**
- [ ] Record action order with timestamps
- [ ] Track action type and amount for each player
- [ ] Maintain action history per betting round
- [ ] Handle out-of-turn actions gracefully
- [ ] Export action sequence in chronological order

**Technical Tasks:**
- [ ] Create `ActionTracker` class
- [ ] Add timestamp to action records
- [ ] Implement action queue per betting round
- [ ] Add action validation logic
- [ ] Integrate with hand state machine
- [ ] Write action tracking tests

**Dependencies:** Story 2.1, Story 1.5
**Assigned To:** [Team Member]

---

### Story 2.3: Continuous Screenshot & Event Loop [8 Story Points]
**Description:** Implement continuous monitoring of poker table
**Acceptance Criteria:**
- [ ] Take screenshots at configurable intervals (e.g., every 500ms)
- [ ] Detect changes in game state automatically
- [ ] Trigger appropriate OCR based on detected changes
- [ ] Handle performance efficiently (don't block)
- [ ] Add start/stop controls

**Technical Tasks:**
- [ ] Create `game_monitor.py` with continuous loop
- [ ] Implement async screenshot capture
- [ ] Add change detection (compare screenshots)
- [ ] Create event dispatcher for game state changes
- [ ] Add configurable polling interval
- [ ] Implement resource cleanup
- [ ] Add threading/async support
- [ ] Write integration tests

**Dependencies:** Story 2.1
**Assigned To:** [Team Member]

---

### Story 2.4: Hand Completion Detection [3 Story Points]
**Description:** Detect when a hand ends and prepare for next hand
**Acceptance Criteria:**
- [ ] Detect showdown or all-fold scenarios
- [ ] Capture final pot winner(s)
- [ ] Reset game state for next hand
- [ ] Trigger data export
- [ ] Handle multi-way pots

**Technical Tasks:**
- [ ] Create hand completion detector
- [ ] Add winner detection logic
- [ ] Implement state reset functionality
- [ ] Add hand summary generation
- [ ] Write completion detection tests

**Dependencies:** Story 2.1, Story 2.2
**Assigned To:** [Team Member]

---

## EPIC 3: Data Storage & CSV Export
**Goal:** Store all captured game data in structured CSV format
**Priority:** HIGH
**Estimated Duration:** 2 weeks

### Story 3.1: Data Model Design [3 Story Points]
**Description:** Design comprehensive data schema for poker hand history
**Acceptance Criteria:**
- [ ] Define CSV schema for hand history
- [ ] Define schema for player actions
- [ ] Define schema for game metadata
- [ ] Document all fields and data types
- [ ] Review and approve with team

**Technical Tasks:**
- [ ] Create data model documentation
- [ ] Define HandHistory dataclass
- [ ] Define PlayerAction dataclass
- [ ] Define GameMetadata dataclass
- [ ] Create schema validation rules
- [ ] Add example CSV files

**Deliverables:**
```
HAND_HISTORY.csv columns:
- hand_id (UUID)
- timestamp
- game_type (e.g., "Hold'em", "Omaha")
- blind_level (e.g., "10/20")
- num_players
- dealer_position
- hero_position
- hero_cards
- board_cards
- pot_size_preflop
- pot_size_flop
- pot_size_turn
- pot_size_river
- final_pot_size
- winner(s)
- hand_result (win/lose/split)

PLAYER_ACTIONS.csv columns:
- hand_id (FK to hand_history)
- timestamp
- betting_round (preflop/flop/turn/river)
- player_position
- player_name
- action_type (fold/check/call/bet/raise/all-in)
- action_amount
- stack_before
- stack_after
- pot_size_before
- pot_size_after
- is_hero (boolean)

GAME_METADATA.csv columns:
- session_id (UUID)
- session_start_time
- session_end_time
- table_name
- total_hands_played
- total_profit_loss
- notes
```

**Dependencies:** EPIC 2
**Assigned To:** [Team Member]

---

### Story 3.2: CSV Writer Module [5 Story Points]
**Description:** Implement CSV export functionality
**Acceptance Criteria:**
- [ ] Export hand history to CSV
- [ ] Export player actions to CSV
- [ ] Export game metadata to CSV
- [ ] Handle file creation and appending
- [ ] Add data validation before export
- [ ] Handle concurrent writes safely

**Technical Tasks:**
- [ ] Create `csv_exporter.py` module
- [ ] Implement HandHistoryWriter class
- [ ] Implement PlayerActionWriter class
- [ ] Add CSV validation logic
- [ ] Add file locking for concurrent access
- [ ] Configure export directory
- [ ] Write CSV export tests

**Dependencies:** Story 3.1
**Assigned To:** [Team Member]

---

### Story 3.3: Real-time Data Logging [3 Story Points]
**Description:** Log data in real-time as hand progresses
**Acceptance Criteria:**
- [ ] Append actions to CSV as they occur
- [ ] Finalize hand record when hand completes
- [ ] Handle interrupted hands gracefully
- [ ] Add data integrity checks
- [ ] Validate CSV format

**Technical Tasks:**
- [ ] Integrate CSV writer with game monitor
- [ ] Add action logging hooks
- [ ] Add hand completion hooks
- [ ] Implement transaction-like hand recording
- [ ] Add error recovery for incomplete hands
- [ ] Write integration tests

**Dependencies:** Story 3.2, Story 2.4
**Assigned To:** [Team Member]

---

### Story 3.4: Data Export Configuration & Controls [2 Story Points]
**Description:** Add UI controls for data export settings
**Acceptance Criteria:**
- [ ] Add export settings to config.yaml
- [ ] Add export directory selection
- [ ] Add enable/disable toggle for logging
- [ ] Add file rotation settings (max file size)
- [ ] Display export status in GUI

**Technical Tasks:**
- [ ] Add export config section to config.yaml
- [ ] Create export settings UI panel
- [ ] Implement file rotation logic
- [ ] Add export status indicator
- [ ] Write config tests

**Dependencies:** Story 3.2
**Assigned To:** [Team Member]

---

## EPIC 4: Data Preprocessing & Feature Engineering
**Goal:** Prepare collected data for neural network training
**Priority:** MEDIUM
**Estimated Duration:** 2-3 weeks

### Story 4.1: Data Cleaning Pipeline [5 Story Points]
**Description:** Clean and validate collected CSV data
**Acceptance Criteria:**
- [ ] Remove incomplete/invalid hands
- [ ] Validate data integrity
- [ ] Handle missing values
- [ ] Detect and flag anomalies
- [ ] Generate data quality report

**Technical Tasks:**
- [ ] Create `data_cleaner.py` module
- [ ] Implement validation rules
- [ ] Add missing value imputation strategies
- [ ] Create anomaly detection logic
- [ ] Generate data quality metrics
- [ ] Write cleaning pipeline tests

**Dependencies:** EPIC 3
**Assigned To:** [Team Member]

---

### Story 4.2: Feature Engineering [8 Story Points]
**Description:** Create neural network features from raw game data
**Acceptance Criteria:**
- [ ] Calculate pot odds for each decision
- [ ] Compute stack-to-pot ratios (SPR)
- [ ] Create position features (early/mid/late)
- [ ] Calculate aggression frequencies
- [ ] Generate player profiling features
- [ ] Encode categorical variables
- [ ] Normalize numeric features

**Technical Tasks:**
- [ ] Create `feature_engineering.py` module
- [ ] Implement pot odds calculator
- [ ] Implement SPR calculator
- [ ] Create position encoder
- [ ] Add player statistics aggregator
- [ ] Implement one-hot encoding for categories
- [ ] Add feature scaling/normalization
- [ ] Document all features
- [ ] Write feature generation tests

**Deliverables:**
```
FEATURES:
- Position features: [is_btn, is_sb, is_bb, is_early, is_mid, is_late]
- Stack features: [stack_bb, spr, stack_percentile]
- Pot features: [pot_odds, pot_size_bb, pot_to_stack_ratio]
- Action features: [vpip, pfr, aggression_factor, cbet_freq]
- Board features: [board_texture, draw_possible, pair_on_board]
- Hand strength: [hand_rank_percentile, hand_category]
- Opponent features: [num_opponents, active_opponents]
- Historical features: [win_rate_last_N, profit_last_N]
```

**Dependencies:** Story 4.1
**Assigned To:** [Team Member]

---

### Story 4.3: Train/Validation/Test Split [2 Story Points]
**Description:** Split dataset for proper ML evaluation
**Acceptance Criteria:**
- [ ] Implement time-based split (no data leakage)
- [ ] Create train (70%), validation (15%), test (15%) sets
- [ ] Ensure session-level splits (no hand leakage)
- [ ] Save split indices for reproducibility
- [ ] Validate split quality

**Technical Tasks:**
- [ ] Create `data_splitter.py` module
- [ ] Implement time-series split logic
- [ ] Add session grouping
- [ ] Save split metadata
- [ ] Write split validation tests

**Dependencies:** Story 4.2
**Assigned To:** [Team Member]

---

### Story 4.4: Data Augmentation [5 Story Points]
**Description:** Augment training data to improve model generalization
**Acceptance Criteria:**
- [ ] Implement position rotation augmentation
- [ ] Add suit isomorphism (card suit swapping)
- [ ] Balance dataset (handle class imbalance)
- [ ] Configure augmentation pipeline
- [ ] Validate augmented data quality

**Technical Tasks:**
- [ ] Create `data_augmentation.py` module
- [ ] Implement position rotation
- [ ] Implement suit isomorphism
- [ ] Add SMOTE for imbalanced classes
- [ ] Create augmentation config
- [ ] Write augmentation tests

**Dependencies:** Story 4.2
**Assigned To:** [Team Member]

---

## EPIC 5: Neural Network Model Development
**Goal:** Build and train neural network for action recommendation
**Priority:** MEDIUM
**Estimated Duration:** 3-4 weeks

### Story 5.1: Model Architecture Design [5 Story Points]
**Description:** Design neural network architecture
**Acceptance Criteria:**
- [ ] Research poker AI architectures
- [ ] Design network topology (layers, neurons, activations)
- [ ] Choose loss function and optimizer
- [ ] Define input/output format
- [ ] Document architecture decisions

**Technical Tasks:**
- [ ] Research existing poker AI models
- [ ] Design DNN architecture (candidate: 3-5 dense layers)
- [ ] Define multi-class output (fold, check, call, bet, raise)
- [ ] Choose framework (PyTorch vs TensorFlow)
- [ ] Create architecture diagram
- [ ] Write architecture documentation

**Deliverables:**
```
Proposed Architecture:
- Input layer: ~50-100 features
- Hidden layer 1: 256 neurons, ReLU, Dropout(0.3)
- Hidden layer 2: 128 neurons, ReLU, Dropout(0.3)
- Hidden layer 3: 64 neurons, ReLU, Dropout(0.2)
- Output layer: 5 neurons (fold, check, call, bet, raise), Softmax
- Loss: Categorical cross-entropy
- Optimizer: Adam
```

**Dependencies:** Story 4.2
**Assigned To:** [Team Member]

---

### Story 5.2: Model Implementation [5 Story Points]
**Description:** Implement neural network in chosen framework
**Acceptance Criteria:**
- [ ] Implement model class
- [ ] Add forward pass logic
- [ ] Add training loop
- [ ] Add validation loop
- [ ] Implement checkpointing
- [ ] Add TensorBoard logging

**Technical Tasks:**
- [ ] Create `poker_nn_model.py` module
- [ ] Implement PokerNetwork class
- [ ] Add training script
- [ ] Add validation metrics
- [ ] Implement model checkpointing
- [ ] Add TensorBoard integration
- [ ] Write model tests

**Dependencies:** Story 5.1
**Assigned To:** [Team Member]

---

### Story 5.3: Training Pipeline [5 Story Points]
**Description:** Create end-to-end training pipeline
**Acceptance Criteria:**
- [ ] Load preprocessed data
- [ ] Create data loaders/batching
- [ ] Train model with hyperparameters
- [ ] Track training metrics
- [ ] Save trained model
- [ ] Generate training report

**Technical Tasks:**
- [ ] Create `train.py` script
- [ ] Implement data loading pipeline
- [ ] Add batch generation logic
- [ ] Implement training loop with logging
- [ ] Add early stopping
- [ ] Create model serialization
- [ ] Write training documentation

**Dependencies:** Story 5.2, Story 4.3
**Assigned To:** [Team Member]

---

### Story 5.4: Model Evaluation [3 Story Points]
**Description:** Evaluate model performance on test set
**Acceptance Criteria:**
- [ ] Calculate accuracy, precision, recall, F1
- [ ] Generate confusion matrix
- [ ] Analyze per-action performance
- [ ] Compare against baseline (GTO charts)
- [ ] Create evaluation report

**Technical Tasks:**
- [ ] Create `evaluate_model.py` script
- [ ] Implement evaluation metrics
- [ ] Generate confusion matrix
- [ ] Create performance visualizations
- [ ] Write evaluation report
- [ ] Compare with baseline strategy

**Dependencies:** Story 5.3
**Assigned To:** [Team Member]

---

### Story 5.5: Hyperparameter Tuning [5 Story Points]
**Description:** Optimize model hyperparameters
**Acceptance Criteria:**
- [ ] Define hyperparameter search space
- [ ] Implement grid/random search
- [ ] Track experiment results
- [ ] Select best configuration
- [ ] Document tuning process

**Technical Tasks:**
- [ ] Set up hyperparameter search framework
- [ ] Define search space (learning rate, layers, dropout, etc.)
- [ ] Run tuning experiments
- [ ] Log results with MLflow or W&B
- [ ] Select and validate best model
- [ ] Write tuning report

**Dependencies:** Story 5.3
**Assigned To:** [Team Member]

---

## EPIC 6: Model Integration & Real-time Inference
**Goal:** Integrate trained model into live application
**Priority:** MEDIUM
**Estimated Duration:** 2 weeks

### Story 6.1: Model Inference Module [3 Story Points]
**Description:** Create module for real-time model predictions
**Acceptance Criteria:**
- [ ] Load trained model
- [ ] Prepare game state features
- [ ] Get action predictions
- [ ] Return confidence scores
- [ ] Handle errors gracefully

**Technical Tasks:**
- [ ] Create `model_inference.py` module
- [ ] Implement model loader
- [ ] Add feature preparation function
- [ ] Implement prediction function
- [ ] Add confidence threshold logic
- [ ] Write inference tests

**Dependencies:** Story 5.3
**Assigned To:** [Team Member]

---

### Story 6.2: GUI Integration [5 Story Points]
**Description:** Display AI recommendations in GUI
**Acceptance Criteria:**
- [ ] Add AI recommendation panel to GUI
- [ ] Show recommended action
- [ ] Display confidence percentage
- [ ] Show alternative actions with probabilities
- [ ] Add enable/disable toggle
- [ ] Update in real-time during game

**Technical Tasks:**
- [ ] Extend run_game_gui.py with AI panel
- [ ] Create recommendation display widget
- [ ] Add confidence bar visualization
- [ ] Implement real-time inference calls
- [ ] Add AI toggle setting
- [ ] Write GUI integration tests

**Dependencies:** Story 6.1
**Assigned To:** [Team Member]

---

### Story 6.3: Performance Optimization [3 Story Points]
**Description:** Optimize inference speed for real-time use
**Acceptance Criteria:**
- [ ] Inference completes in <100ms
- [ ] No UI blocking during inference
- [ ] Efficient model loading (cache)
- [ ] Profile and optimize bottlenecks
- [ ] Measure and document performance

**Technical Tasks:**
- [ ] Profile inference pipeline
- [ ] Optimize feature preparation
- [ ] Add model caching
- [ ] Implement async inference
- [ ] Run performance benchmarks
- [ ] Write optimization report

**Dependencies:** Story 6.1
**Assigned To:** [Team Member]

---

### Story 6.4: Action Explanation Module [5 Story Points]
**Description:** Provide explanations for AI recommendations
**Acceptance Criteria:**
- [ ] Explain why action was recommended
- [ ] Show key contributing features
- [ ] Display relevant statistics
- [ ] Add explainability UI
- [ ] Support multiple explanation types

**Technical Tasks:**
- [ ] Implement SHAP or LIME explainability
- [ ] Create explanation generator
- [ ] Add feature importance display
- [ ] Create explanation UI panel
- [ ] Write explanation tests

**Dependencies:** Story 6.1
**Assigned To:** [Team Member]

---

## EPIC 7: Testing, Documentation & Deployment
**Goal:** Ensure production-ready quality
**Priority:** LOW (parallel to other epics)
**Estimated Duration:** Ongoing

### Story 7.1: Unit Test Coverage [8 Story Points]
**Description:** Achieve >80% unit test coverage
**Acceptance Criteria:**
- [ ] Write unit tests for all core modules
- [ ] Achieve >80% code coverage
- [ ] Add continuous integration (CI)
- [ ] All tests pass consistently
- [ ] Generate coverage report

**Technical Tasks:**
- [ ] Write tests for OCR modules
- [ ] Write tests for game state logic
- [ ] Write tests for CSV export
- [ ] Write tests for feature engineering
- [ ] Write tests for model inference
- [ ] Set up pytest-cov
- [ ] Configure GitHub Actions CI
- [ ] Generate coverage badge

**Dependencies:** All prior stories
**Assigned To:** [Team Member]

---

### Story 7.2: Integration Tests [5 Story Points]
**Description:** Test end-to-end workflows
**Acceptance Criteria:**
- [ ] Test complete hand capture workflow
- [ ] Test CSV export workflow
- [ ] Test model inference workflow
- [ ] Test GUI interactions
- [ ] All integration tests pass

**Technical Tasks:**
- [ ] Create integration test suite
- [ ] Write end-to-end capture tests
- [ ] Write end-to-end inference tests
- [ ] Create test fixtures (screenshots)
- [ ] Set up test database/CSV
- [ ] Run integration tests in CI

**Dependencies:** EPIC 6
**Assigned To:** [Team Member]

---

### Story 7.3: User Documentation [5 Story Points]
**Description:** Create comprehensive user documentation
**Acceptance Criteria:**
- [ ] Update README with new features
- [ ] Create setup guide
- [ ] Create calibration guide
- [ ] Create data collection guide
- [ ] Create AI training guide
- [ ] Add troubleshooting section

**Technical Tasks:**
- [ ] Update README.md
- [ ] Create SETUP_GUIDE.md
- [ ] Create DATA_COLLECTION_GUIDE.md
- [ ] Create AI_TRAINING_GUIDE.md
- [ ] Create TROUBLESHOOTING.md
- [ ] Add screenshots/diagrams
- [ ] Review documentation

**Dependencies:** EPIC 6
**Assigned To:** [Team Member]

---

### Story 7.4: Code Quality Improvements [5 Story Points]
**Description:** Implement code quality improvements from audit
**Acceptance Criteria:**
- [ ] Replace all print() with logging
- [ ] Remove dead code (card_display.py, etc.)
- [ ] Add type hints to all functions
- [ ] Fix code duplication
- [ ] Refactor long methods
- [ ] Pass linting checks

**Technical Tasks:**
- [ ] Add logging module configuration
- [ ] Replace print statements with logging
- [ ] Remove unused files
- [ ] Add type hints throughout
- [ ] Refactor duplicate code
- [ ] Break up long methods
- [ ] Run pylint/flake8
- [ ] Fix all linting errors

**Dependencies:** None (can start immediately)
**Assigned To:** [Team Member]

---

### Story 7.5: Deployment Package [3 Story Points]
**Description:** Create distributable package
**Acceptance Criteria:**
- [ ] Create setup.py
- [ ] Add requirements.txt with all deps
- [ ] Create Docker container (optional)
- [ ] Add installation script
- [ ] Test installation on clean system

**Technical Tasks:**
- [ ] Create setup.py
- [ ] Update requirements.txt
- [ ] Create Dockerfile
- [ ] Write install.sh script
- [ ] Test on Windows/Mac/Linux
- [ ] Write deployment documentation

**Dependencies:** Story 7.3
**Assigned To:** [Team Member]

---

## SPRINT PLANNING RECOMMENDATIONS

### Sprint 1 (2 weeks) - Foundation
- Story 1.1: Player Position Detection
- Story 1.2: Dealer Button Detection
- Story 7.4: Code Quality Improvements (parallel)

### Sprint 2 (2 weeks) - Core Data Capture
- Story 1.3: Pot Size OCR
- Story 1.4: Player Stack Size OCR
- Story 1.5: Bet/Action Amount Detection
- Story 1.6: Blind Level Detection

### Sprint 3 (2 weeks) - Game State Management
- Story 2.1: Hand State Machine
- Story 2.2: Action Sequence Tracking
- Story 2.3: Continuous Screenshot & Event Loop

### Sprint 4 (2 weeks) - Data Export
- Story 2.4: Hand Completion Detection
- Story 3.1: Data Model Design
- Story 3.2: CSV Writer Module
- Story 3.3: Real-time Data Logging

### Sprint 5 (2 weeks) - Data Preparation
- Story 3.4: Data Export Configuration
- Story 4.1: Data Cleaning Pipeline
- Story 4.2: Feature Engineering (start)

### Sprint 6 (2 weeks) - Feature Engineering Complete
- Story 4.2: Feature Engineering (complete)
- Story 4.3: Train/Validation/Test Split
- Story 4.4: Data Augmentation

### Sprint 7 (2 weeks) - Model Development
- Story 5.1: Model Architecture Design
- Story 5.2: Model Implementation
- Story 5.3: Training Pipeline (start)

### Sprint 8 (2 weeks) - Model Training & Evaluation
- Story 5.3: Training Pipeline (complete)
- Story 5.4: Model Evaluation
- Story 5.5: Hyperparameter Tuning

### Sprint 9 (2 weeks) - Integration
- Story 6.1: Model Inference Module
- Story 6.2: GUI Integration
- Story 6.3: Performance Optimization

### Sprint 10 (2 weeks) - Polish & Deploy
- Story 6.4: Action Explanation Module
- Story 7.1: Unit Test Coverage
- Story 7.2: Integration Tests
- Story 7.3: User Documentation
- Story 7.5: Deployment Package

---

## RISK MANAGEMENT

### High Risk Items:
1. **OCR Accuracy:** May need multiple iterations to achieve >90% accuracy
   - **Mitigation:** Build robust calibration tools, use high-quality screenshots

2. **Real-time Performance:** Continuous monitoring may impact system performance
   - **Mitigation:** Optimize code, use async operations, add configurable intervals

3. **Data Volume:** May collect insufficient data for training
   - **Mitigation:** Run data collection for extended period, use data augmentation

4. **Model Performance:** Initial model may not outperform baseline
   - **Mitigation:** Start with simple model, iterate based on results, consider ensemble methods

### Medium Risk Items:
1. **ClubGG UI Changes:** Poker client updates may break OCR
   - **Mitigation:** Make calibration easy to re-run, version control calibration configs

2. **Hardware Requirements:** Model training may require GPU
   - **Mitigation:** Use cloud GPU resources (Colab, AWS), optimize model size

---

## SUCCESS METRICS

### Phase 1 (Data Collection):
- [ ] Capture 1000+ complete hands with >95% accuracy
- [ ] All table elements detected correctly
- [ ] Clean CSV export with no data loss

### Phase 2 (Model Training):
- [ ] Model accuracy >60% on test set
- [ ] Model performs better than random baseline
- [ ] Inference time <100ms per prediction

### Phase 3 (Deployment):
- [ ] Real-time recommendations working in GUI
- [ ] No crashes during 100-hand session
- [ ] User feedback positive

---

## TECHNICAL STACK

### Current:
- Python 3.7+
- Tesseract OCR
- OpenCV/Pillow
- PyAutoGUI
- Tkinter
- PyYAML

### To Add:
- **ML Framework:** PyTorch or TensorFlow
- **Data Processing:** Pandas, NumPy, Scikit-learn
- **Visualization:** Matplotlib, Seaborn, TensorBoard
- **Testing:** pytest, pytest-cov, pytest-mock
- **Logging:** Python logging module
- **Experiment Tracking:** MLflow or Weights & Biases
- **CI/CD:** GitHub Actions
- **Optional:** Docker, FastAPI (for model serving)

---

## NOTES FOR JIRA SETUP

1. **Epic Naming:** Use format "EPIC-N: [Name]"
2. **Story Naming:** Use format "STORY-N.N: [Name]"
3. **Labels:** Add labels like `ocr`, `ml`, `data`, `gui`, `testing`
4. **Priority:** Set based on dependencies and business value
5. **Story Points:** Use Fibonacci scale (1, 2, 3, 5, 8, 13)
6. **Acceptance Criteria:** Checkboxes can become Jira subtasks
7. **Dependencies:** Link stories with "blocks"/"is blocked by"

---

**Document Version:** 1.0
**Last Updated:** 2025-12-09
**Next Review:** After Sprint 1
