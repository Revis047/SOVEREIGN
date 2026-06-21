using LinearAlgebra

"""
    score_signal(signal_features::Vector{Float64}, weights::Vector{Float64})

Calculates the commercial heat of a signal based on multi-dimensional features:
1. Velocity (trending speed)
2. Intent (buyer vs researcher)
3. Pain Intensity (emotional/urgent language density)
4. Market Gap (lack of existing solutions)
5. ICP Overlap (alignment with target profile)
"""
function score_signal(features::Vector{Float64}, weights::Vector{Float64})
    if length(features) != length(weights)
        throw(ArgumentError("Features and weights must have same length"))
    end

    # Dot product for baseline score
    raw_score = dot(features, weights)

    # Non-linear scaling (e.g., sigmoid) to normalize to [0, 1]
    return 1.0 / (1.0 + exp(-raw_score))
end

"""
    rank_signals(signals::Matrix{Float64}, weights::Vector{Float64})

Ranks a batch of signals by commercial heat.
"""
function rank_signals(signals::Matrix{Float64}, weights::Vector{Float64})
    num_signals = size(signals, 1)
    scores = [score_signal(signals[i, :], weights) for i in 1:num_signals]

    # Sort indices by score descending
    return sortperm(scores, rev=true), scores
end

# Example usage for testing
# signals = [0.8 0.9 0.7 0.5 0.9;  # Signal A: High velocity, high pain
#            0.2 0.3 0.1 0.9 0.2]  # Signal B: Low heat
# weights = [0.2, 0.2, 0.3, 0.2, 0.1]
# indices, final_scores = rank_signals(signals, weights)
